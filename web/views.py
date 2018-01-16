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

def test(request):
    return render(request, "test.html",context={})
