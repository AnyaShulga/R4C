import json
import os
import datetime
import sys

import openpyxl
from django.core.exceptions import FieldDoesNotExist
from django.db.models import Q, Count
from django.http import HttpResponse
from django.utils import timezone

from R4C.settings import BASE_DIR
from robots.models import Robot

sys.path.append('/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/site-packages')

# Create your views here.
def manufactured_robot(request):
    if request.method == 'POST':
        input_data = json.loads(request.body)
    for key, value in input_data.items():
        try:
            Robot._meta.get_field(key)
        except FieldDoesNotExist:
            return HttpResponse('Входные данные не соотвествуют модели.')
    serial = f'{input_data["model"]} - {input_data["version"]}'
    new_robot = Robot.objects.create(serial=serial, model=input_data["model"], version=input_data["version"], created=input_data["created"])
    new_robot.save()
    return HttpResponse(new_robot)