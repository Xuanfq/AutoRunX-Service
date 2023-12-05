from . import utils
from django.http import JsonResponse
from django.contrib import auth
import json
from . import models

from .manager import tokencenter


# auth/token
def token(request):
    return login(request)


# auth/login
def login(request):
    """
    POST: {data:{username:'',password:''}}
    GET: ?username=xxx&password=xxx
    """
    if utils.is_method_POST(request):
        _data = json.loads(request.body)["data"]
        username = _data['username']
        password = _data['password']
    elif utils.is_method_GET(request):
        username = request.GET.get("username")
        password = request.GET.get("password")
    else:
        return JsonResponse({"flag": False, "data": "Error Request Method"})
    user = auth.authenticate(request, username=username, password=password)
    if user is None:
        return JsonResponse({"flag": False, "data": None})
    # log
    models.ActionLog(owner=user,
                            action='login',
                            action_type='auth',
                            action_data='').save()
    return JsonResponse({"flag": True, "data": tokencenter.generate_token(username)})


def verify(request):
    token = request.META.get('HTTP_TOKEN')
    if token is None:
        return (False, "The identity token is missing")
    return tokencenter.verify_token(token)

