
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
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


# actionlog/get
def get(request):
    """
    get: null | uri?action=xxx
    params: [action]
    """
    if not utils.is_method_GET(request):
        return JsonResponse({"flag": False, "data": "Error Request Method"})
    user = request.META['API_AUTH_USER']
    action = request.GET.get('action', '')
    action_type = request.GET.get('action_type', '')
    mark = request.GET.get('mark', '')
    page = request.GET.get('page', 1)
    limit = request.GET.get('limit', 10)
    queryset = models.ActionLog.objects.filter(owner=user,
                                               action__icontains=action,
                                               action_data__icontains=action,
                                               action_type__icontains=action_type,
                                               mark__icontains=mark,
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
    for actionlogdata in query_result:
        result["list"].append({
            "id": str(actionlogdata.id),
            "owner": actionlogdata.owner.username,
            "action": actionlogdata.action,
            "action_type": actionlogdata.action_type,
            "action_data": str(actionlogdata.action_data),
            "mark": actionlogdata.mark,
            "update_time": utils.datetime2jsobject(actionlogdata.update_time),
            "create_time": utils.datetime2jsobject(actionlogdata.create_time),
        })
    return JsonResponse({"flag": True, "data": result})
