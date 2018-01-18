from django.shortcuts import render
from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponse
import os
import json
from web.models import Car
from datetime import datetime
def index(request):
    AllCar=Car.objects.all()
    return render(request, "index.html",context={'AllCar':AllCar})

def change_route(request):
    num=request.GET.get('num')
    car = Car.objects.filter(plate_number=num)
    point=[]
    point_time=[]
    for i in car:
        point=i.point.split('^')
        point_time=i.point_time.split("^")
    response_data={'point':point,'point_time':point_time}
    return HttpResponse(json.dumps(response_data), content_type="application/json")

def test(request):
    return render(request, "test.html",context={})
