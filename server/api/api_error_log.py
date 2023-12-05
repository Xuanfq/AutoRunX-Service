
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


# errorlog/get
def get(request):
    """
    get: null | uri?error=xxx
    params: [error]
    """
    if not utils.is_method_GET(request):
        return JsonResponse({"flag": False, "data": "Error Request Method"})
    user = request.META['API_AUTH_USER']
    error = request.GET.get('error', '')
    error_type = request.GET.get('error_type', '')
    mark = request.GET.get('mark', '')
    page = request.GET.get('page', 1)
    limit = request.GET.get('limit', 10)
    queryset = models.ErrorLog.objects.filter(owner=user,
                                         error__icontains=error,
                                         error_data__icontains=error,
                                         error_type__icontains=error_type,
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
    for errorlogdata in query_result:
        result["list"].append({
            "id": str(errorlogdata.id),
            "owner": errorlogdata.owner.username,
            "error": errorlogdata.error,
            "error_type": errorlogdata.error_type,
            "error_data": str(errorlogdata.error_data),
            "mark": errorlogdata.mark,
            "update_time": utils.datetime2jsobject(errorlogdata.update_time),
            "create_time": utils.datetime2jsobject(errorlogdata.create_time),
        })
    return JsonResponse({"flag": True, "data": result})
























