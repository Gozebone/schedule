from django.shortcuts import render

# Create your views here.

import json
from django.contrib.auth.models import User #####
from django.http import JsonResponse , HttpResponse ####
from calendar_logic.add_events import add_events

def index(request):
    return HttpResponse("Hello, world. You're at the index.")


def create_events(request):
    name = request.GET.get('name', None)
    password = request.GET.get('password', None)
    group = request.GET.get('group', None)

    add_events(group)

    data = {
        'summary': "calendar created",
        'raw': 'Successful',
    }

    return JsonResponse(data)
    