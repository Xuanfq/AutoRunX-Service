from django.http import JsonResponse
from django.contrib import auth
import json
from . import api_auth
from . import utils
from django.contrib.auth.models import User


# user/login
def login(request):
    return api_auth.login(request)


# user/info
def get_info(request):
    """
    get: 
    """
    if not utils.is_method_GET(request):
        return JsonResponse({"flag": False, "data": "Error Request Method"})
    user = request.META['API_AUTH_USER']
    # user = User(user)
    groups = [str(group).replace('api-','') for group in user.groups.all()]
    permissions = [str(permission).replace('api.', '')
                   for permission in user.get_all_permissions() if str(permission).startswith('api')]
    info = {
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'groups': groups,
        'roles': groups,
        'permissions': permissions,
        'is_staff': user.is_staff,
        'is_active': user.is_active,
        'is_superuser': user.is_superuser,
        'last_login': user.last_login,
        'date_joined': user.date_joined,
    }
    return JsonResponse({"flag": True, "data": info})
