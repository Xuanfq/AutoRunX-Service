from django.shortcuts import render

# Create your views here.

from django.http import JsonResponse
import json


def hello(request):
    return JsonResponse({"flag": True, "data": "Hello AutoRunX!"})

