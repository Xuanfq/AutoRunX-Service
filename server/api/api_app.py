
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
import pytz
from . import models
import json
import os
from . import utils
from django.contrib import auth
from django.contrib.auth.models import User
from datetime import datetime
from .forms import AppRunConfigUploadModelForm
from .models import App, ActionLog, ErrorLog
from django.db import transaction
from django.utils import timezone
from django.http import HttpResponse, Http404, FileResponse
from .manager import appmanager


# app/add
def add(request):
    """
    post: {data:[]} | {data:{}}
    params: name
    """
    if not utils.is_method_POST(request):
        return JsonResponse({"flag": False, "data": "Error Request Method"})
    _data = json.loads(request.body)["data"]
    data = _data if isinstance(_data, list) else [_data]
    user = request.META['API_AUTH_USER']
    for appdata in data:
        appname = appdata['name']
        if len(appname) == 0:
            return JsonResponse({"flag": False, "data": "Error Request Parameters"})
        with transaction.atomic():
            app_query_result = models.App.objects.filter(
                owner=user, name=appname, delete_time=None)
            if len(app_query_result) > 0:
                return JsonResponse({"flag": False, "data": "An app of this name already exists in your account"})
            appdata = models.App(name=appname,
                                 owner=user,
                                 upload_run_config=False)
            appdata.save()
        # log
        models.ActionLog(owner=user,
                         action='addApp',
                         action_type='app',
                         action_data='id=%s,name=%s' % (appdata.id, appname)).save()
    return JsonResponse({"flag": True, "data": None})


# app/delete
def delete(request):
    """
    post: {data:[]} | {data:{}}
    params: id
    """
    if not utils.is_method_POST(request):
        return JsonResponse({"flag": False, "data": "Error Request Method"})
    _data = json.loads(request.body)["data"]
    data = _data if isinstance(_data, list) else [_data]
    user = request.META['API_AUTH_USER']
    for appdata in data:
        appid = appdata['id']
        if len(appid) == 0:
            return JsonResponse({"flag": False, "data": "Error Request Parameters"})
        with transaction.atomic():
            app_query_result = models.App.objects.filter(
                owner=user, id=appid, delete_time=None)
            if len(app_query_result) == 0:
                return JsonResponse({"flag": False, "data": "The app does not exist"})
            app = app_query_result[0]
            # is app running or planning
            if appmanager.exist(app.id):
                # ...
                return JsonResponse({"flag": False, "data": "The app is in running or planning status"})
            # delete file
            # ...
            app.delete()
        # log
        models.ActionLog(owner=user,
                         action='deleteApp',
                         action_type='app',
                         action_data='id=%s' % appid,).save()
    return JsonResponse({"flag": True, "data": None})


# app/update/runconfig/upload
def update_runconfig_upload(request):
    """
    post: uri?id=xxx
    params: id
    """
    if not utils.is_method_POST(request):
        return JsonResponse({"flag": False, "data": "Error Request Method"})
    id = request.GET.get('id', None)
    if id is None:
        return JsonResponse({"flag": False, "data": "Required parameter missing"})
    user = request.META['API_AUTH_USER']
    with transaction.atomic():
        app_query_result = models.App.objects.filter(
            owner=user, id=id, delete_time=None)
        if len(app_query_result) == 0:
            return JsonResponse({"flag": False, "data": "The app does not exist"})
        app = app_query_result[0]
        run_config_form = AppRunConfigUploadModelForm(request.POST,
                                                      request.FILES,
                                                      instance=app)
        if not run_config_form.is_valid():
            return JsonResponse({"flag": False, "data": "Invalid Form Data"})
        if app.plan_start_time is not None:
            return JsonResponse({"flag": False, "data": "The app is scheduled to run and cannot be modified"})
        if app.end_running_time is not None:
            return JsonResponse({"flag": False, "data": "The app is finished and cannot be modified"})
        if app.start_running_time is not None:
            return JsonResponse({"flag": False, "data": "The app is running and cannot be modified"})
        # delete old
        models.App.objects.filter(owner=user, id=id, delete_time=None)[
            0].run_config_file.delete(True)
        # save new
        app.upload_run_config = True
        run_config_form.save()
    # log
    models.ActionLog(owner=user,
                     action='uploadAppRunConfig',
                     action_type='app',
                     action_data='id=%s' % id,).save()
    return JsonResponse({"flag": True, "data": None})


# app/update/runconfig/delete
def update_runconfig_delete(request):
    """
    post: uri?id=xxx
    params: id
    """
    if not utils.is_method_POST(request):
        return JsonResponse({"flag": False, "data": "Error Request Method"})
    id = request.GET.get('id', None)
    if id is None:
        return JsonResponse({"flag": False, "data": "Required parameter missing"})
    user = request.META['API_AUTH_USER']
    with transaction.atomic():
        app_query_result = models.App.objects.filter(
            owner=user, id=id, delete_time=None)
        if len(app_query_result) == 0:
            return JsonResponse({"flag": False, "data": "The app does not exist"})
        app = app_query_result[0]
        if app.plan_start_time is not None:
            return JsonResponse({"flag": False, "data": "The app is scheduled to run and cannot be modified"})
        # delete
        app.upload_run_config = False
        app.run_config_file.delete()
        app.save()
    # log
    models.ActionLog(owner=user,
                     action='deleteAppRunConfig',
                     action_type='app',
                     action_data='id=%s' % id,).save()
    return JsonResponse({"flag": True, "data": None})


# app/update/name
def update_name(request):
    """
    post: {data:[]} | {data:{}}
    params: id, name
    """
    if not utils.is_method_POST(request):
        return JsonResponse({"flag": False, "data": "Error Request Method"})
    _data = json.loads(request.body)["data"]
    data = _data if isinstance(_data, list) else [_data]
    user = request.META['API_AUTH_USER']
    for appdata in data:
        appid = appdata['id']
        appname = appdata['name']
        if len(appname) == 0:
            return JsonResponse({"flag": False, "data": "Error Request Parameters"})
        with transaction.atomic():
            app_query_result = models.App.objects.filter(
                owner=user, name=appname, delete_time=None)
            if len(app_query_result) > 0:
                return JsonResponse({"flag": False, "data": "An app of this name already exists in your account"})
            app_query_result = models.App.objects.filter(
                owner=user, id=appid, delete_time=None)
            if len(app_query_result) == 0:
                return JsonResponse({"flag": False, "data": "The app does not exist"})
            app = app_query_result[0]
            if app.plan_start_time is not None:
                return JsonResponse({"flag": False, "data": "The app is scheduled to run and cannot be modified"})
            app.name = appname
            app.save()
        # log
        models.ActionLog(owner=user,
                         action='updateAppName',
                         action_type='app',
                         action_data='id=%s,name=%s' % (appid, appname)).save()
    return JsonResponse({"flag": True, "data": None})


# app/update/mark
def update_mark(request):
    """
    post: {data:[]} | {data:{}}
    params: id, name
    """
    if not utils.is_method_POST(request):
        return JsonResponse({"flag": False, "data": "Error Request Method"})
    _data = json.loads(request.body)["data"]
    data = _data if isinstance(_data, list) else [_data]
    user = request.META['API_AUTH_USER']
    for appdata in data:
        appid = appdata['id']
        appmark = appdata['mark']
        with transaction.atomic():
            app_query_result = models.App.objects.filter(
                owner=user, id=appid, delete_time=None)
            if len(app_query_result) == 0:
                return JsonResponse({"flag": False, "data": "The app does not exist"})
            app = app_query_result[0]
            app.mark = appmark
            app.save()
        # log
        models.ActionLog(owner=user,
                         action='updateAppMark',
                         action_type='app',
                         action_data='id=%s,mark=%s' % (appid, appmark)).save()
    return JsonResponse({"flag": True, "data": None})


# app/update/planstart
def update_planstart(request):
    """
    post: {data:[]} | {data:{}}
    params: id, plan_start_time
    """
    if not utils.is_method_POST(request):
        return JsonResponse({"flag": False, "data": "Error Request Method"})
    _data = json.loads(request.body)["data"]
    data = _data if isinstance(_data, list) else [_data]
    user = request.META['API_AUTH_USER']
    for appdata in data:
        appid = appdata['id']
        plan_start_time = appdata['plan_start_time']
        if plan_start_time is not None:
            try:
                plan_start_time = datetime.fromtimestamp(
                    int(plan_start_time/1000))
            except Exception as e:
                return JsonResponse({"flag": False, "data": "Error Request Parameters"})
            if plan_start_time < datetime.now():
                return JsonResponse({"flag": False, "data": "Invalid Time For Planning To Start"})
        with transaction.atomic():
            app_query_result = models.App.objects.filter(
                owner=user, id=appid, delete_time=None)
            if len(app_query_result) == 0:
                return JsonResponse({"flag": False, "data": "The app does not exist"})
            app = app_query_result[0]
            if not app.upload_run_config:
                return JsonResponse({"flag": False, "data": "The app has not uploaded the running configuration file"})
            if app.end_running_time is not None:
                return JsonResponse({"flag": False, "data": "The app is finished"})
            if app.start_running_time is not None:
                return JsonResponse({"flag": False, "data": "The app is running"})
            app.plan_start_time = plan_start_time
            app.save()
            # plan to start
            flag = appmanager.create(app)
            if not flag:
                return JsonResponse({"flag": False, "data": "The number of running apps reaches the threshold"})
            appmanager.schedule(app.id, plan_start_time)
        # log
        models.ActionLog(owner=user,
                         action='planStartApp',
                         action_type='app',
                         action_data='id=%s,plan_start_time=%s' % (appid, plan_start_time)).save()
    return JsonResponse({"flag": True, "data": None})


# app/update/start
def update_start(request):
    """
    post: {data:[]} | {data:{}}
    params: id
    """
    if not utils.is_method_POST(request):
        return JsonResponse({"flag": False, "data": "Error Request Method"})
    _data = json.loads(request.body)["data"]
    data = _data if isinstance(_data, list) else [_data]
    user = request.META['API_AUTH_USER']
    for appdata in data:
        appid = appdata['id']
        with transaction.atomic():
            app_query_result = models.App.objects.filter(
                owner=user, id=appid, delete_time=None)
            if len(app_query_result) == 0:
                return JsonResponse({"flag": False, "data": "The app does not exist"})
            app = app_query_result[0]
            if not app.upload_run_config:
                return JsonResponse({"flag": False, "data": "The app has not uploaded the running configuration file"})
            if app.end_running_time is not None:
                return JsonResponse({"flag": False, "data": "The app is finished"})
            if app.start_running_time is not None:
                return JsonResponse({"flag": False, "data": "The app is running"})
            app.plan_start_time = datetime.now()
            # app.start_running_time = app.plan_start_time finish in start callback
            # app.save()
            # run start and clear plan timer
            flag = appmanager.create(app)
            if not flag:
                return JsonResponse({"flag": False, "data": "The number of running apps reaches the threshold"})
            appmanager.start(str(app.id))
        # log
        models.ActionLog(owner=user,
                         action='startApp',
                         action_type='app',
                         action_data='id=%s' % (appid)).save()
    return JsonResponse({"flag": True, "data": None})


# app/update/abort
def update_abort(request):
    """
    post: {data:[]} | {data:{}}
    params: id
    """
    if not utils.is_method_POST(request):
        return JsonResponse({"flag": False, "data": "Error Request Method"})
    _data = json.loads(request.body)["data"]
    data = _data if isinstance(_data, list) else [_data]
    user = request.META['API_AUTH_USER']
    for appdata in data:
        appid = appdata['id']
        with transaction.atomic():
            app_query_result = models.App.objects.filter(
                owner=user, id=appid, delete_time=None)
            if len(app_query_result) == 0:
                return JsonResponse({"flag": False, "data": "The app does not exist"})
            app = app_query_result[0]
            if app.end_running_time is not None:
                return JsonResponse({"flag": False, "data": "The app is finished"})
            if app.start_running_time is None:
                return JsonResponse({"flag": False, "data": "The app isn't running yet"})
            # update in the callback function
            # app.abort_running_time = timezone.now()
            # app.end_running_time = app.abort_running_time
            # app.save()
            # run abort
            appmanager.abort(app.id)
        # log
        models.ActionLog(owner=user,
                         action='abortApp',
                         action_type='app',
                         action_data='id=%s' % (appid)).save()
    return JsonResponse({"flag": True, "data": None})


def download_result(request):
    if not utils.is_method_GET(request):
        return JsonResponse({"flag": False, "data": "Error Request Method"})
    user = request.META['API_AUTH_USER']
    id = request.GET.get('id', None)
    name = request.GET.get('name', None)
    if id is not None:
        queryset = models.App.objects.filter(
            owner=user, id=id, delete_time=None)
    elif name is not None:
        queryset = models.App.objects.filter(
            owner=user, name=name, delete_time=None)
    else:
        return JsonResponse({"flag": False, "data": "Error Request Parameters"})
    app = queryset[0]
    if app.end_running_time is None:
        return JsonResponse({"flag": False, "data": "The app is not finished"})
    result_file_path = os.path.join(
        os.getcwd(), 'media/app', str(app.id), '{}.zip'.format(str(app.id)))
    response = FileResponse(open(result_file_path, 'rb'))
    response['content_type'] = "application/octet-stream"
    response['Content-Disposition'] = os.path.basename(result_file_path)
    # log
    models.ActionLog(owner=user,
                     action='downloadAppRunRusult',
                     action_type='app',
                     action_data='id=%s' % (id)).save()
    return response


# app/get
def get(request):
    """
    get: null | uri?name=xxx
    params: [name]
    """
    if not utils.is_method_GET(request):
        return JsonResponse({"flag": False, "data": "Error Request Method"})
    user = request.META['API_AUTH_USER']
    name = request.GET.get('name', '')
    mark = request.GET.get('mark', '')
    run_time_error = request.GET.get('run_time_error', '')
    page = request.GET.get('page', 1)
    limit = request.GET.get('limit', 10)
    queryset = models.App.objects.filter(owner=user,
                                         name__icontains=name,
                                         mark__icontains=mark,
                                         run_time_error__icontains=run_time_error,
                                         delete_time=None).order_by('create_time')
    query_result = []
    result = {'list': [], 'page': page, 'limit': limit, 'total': 0}
    if limit is not None:
        try:
            limit = int(limit)
            page = int(page)
        except:
            return JsonResponse({"flag": False, "data": "Error Request Parameters"})
        if limit < 1 or page < 1:
            return JsonResponse({"flag": False, "data": "Error Request Parameters"})
        paginator = Paginator(queryset, limit)
        result["total"] = paginator.count
        result["page"] = min(paginator.num_pages, page)
        query_result = paginator.page(result["page"])
    for appdata in query_result:
        result["list"].append({
            "id": str(appdata.id),
            "owner": appdata.owner.username,
            "name": appdata.name,
            "upload_run_config": appdata.upload_run_config,
            "run_config_file": str(appdata.run_config_file),
            "plan_start_time": utils.datetime2jsobject(appdata.plan_start_time),
            "start_running_time": utils.datetime2jsobject(appdata.start_running_time),
            "end_running_time": utils.datetime2jsobject(appdata.end_running_time),
            "abort_running_time": utils.datetime2jsobject(appdata.abort_running_time),
            "run_time_error": appdata.run_time_error,
            "mark": appdata.mark,
            "update_time": utils.datetime2jsobject(appdata.update_time),
            "create_time": utils.datetime2jsobject(appdata.create_time),
        })
    return JsonResponse({"flag": True, "data": result})
