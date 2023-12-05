from django.shortcuts import HttpResponseRedirect
from django.http import JsonResponse
import json
from django.utils.deprecation import MiddlewareMixin
import re
from . import api_auth
from django.contrib.auth.models import User
import logging
import traceback
logger = logging.getLogger('default')

GATEWAY_01_WHITELIST = [
    '/admin/*',
    '/api/auth/login',
    '/api/auth/token',
    '/api/user/login',
    '/ws',
]

GATEWAY_01_PERMISSION = {
    '/api/node/get': 'api.view_node',
    '/api/node/add': 'api.add_node',
    '/api/node/delete': 'api.delete_node',
    '/api/app/get': 'api.view_app',
    '/api/app/download/result': 'api.view_app',
    '/api/app/add': 'api.add_app',
    '/api/app/update/*': 'api.change_app',
    '/api/app/delete': 'api.delete_app',
    '/api/errorlog/get': 'api.view_errorlog',
}


class ApiMiddleware(MiddlewareMixin):
    def process_request(self, request):
        """
        auth
        """
        path = request.path
        # white list path
        for pattern in GATEWAY_01_WHITELIST:
            if re.match(pattern, path):
                return
        # auth token
        flag, data = api_auth.verify(request)
        if flag:
            user = User.objects.filter(username=data)[0]
            request.META['API_AUTH_USERNAME'] = data
            request.META['API_AUTH_USER'] = user
        else:
            return JsonResponse({"flag": False, "data": data})
        # auth permission
        for key, value in GATEWAY_01_PERMISSION.items():
            if re.match(key, path):
                if user.has_perm(value) if isinstance(value, str) else user.has_perms(value):
                    return
                else:
                    return JsonResponse({"flag": False, "data": 'Permission Denied'})

    def process_exception(self, request, exception):
        path = request.path
        for pattern in GATEWAY_01_WHITELIST:
            if re.match(pattern, path):
                return
        logger.error("Request Error: {}\n{}".format(request.path, exception))
        return JsonResponse({"flag": False, "data": "Request Error: {}".format(str(exception))})
