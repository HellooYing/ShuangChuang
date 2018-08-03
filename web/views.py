from django.shortcuts import render
from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponse
import os
import json
from web.models import Car, Feature, Tracking
from datetime import datetime


def index(request):
    AllCar = Car.objects.all()
    return render(request, "index.html", context={'AllCar': AllCar})


def change_route(request):
    num = request.GET.get('num')
    car = Car.objects.filter(plate_number=num)
    point = []
    point_time = []
    for i in car:
        point = i.point.split('^')
        point_time = i.point_time.split("^")
    response_data = {'point': point, 'point_time': point_time}
    return HttpResponse(json.dumps(response_data), content_type="application/json")

def new(request):
    a=Feature()
    a.number = request.GET.get("number")
    a.time = request.GET.get("time")
    a.location = request.GET.get("location")
    a.color = request.GET.get("color")
    a.kind = request.GET.get("kind")
    a.save()
    resp = {"msg": "上传成功！"}
    return HttpResponse(json.dumps(resp), content_type="application/json")


def upload(request):
    # 接收上传的信息
    time = request.GET.get("time")
    location = request.GET.get("location")
    color = request.GET.get("color")
    kind = request.GET.get("kind")
    # 找出特征库中最早入库的颜色种类一致的那个，原理是先到树莓派1的也会先到2，除非超车。
    # 如果特征库没有，这条特征就是识别错了的
    try:
        l = Feature.objects.filter(kind=kind, color=color)
    except:
        l = 0
    if l==0:
        resp = {"msg": "无此特征！"}
        return HttpResponse(json.dumps(resp), content_type="application/json")
    else:
        a = l[0]
        # 找出轨迹库中对应的轨迹，加点更新
        b = Tracking.objects.get(number=a.number)
        b.location = b.location+","+location
        b.time = b.time+","+time
        b.save()
        # 删除上一条特征，加入本条特征
        c=Feature()
        c.number = a.number
        c.time = time
        c.location = location
        c.color = color
        c.kind = kind
        c.save()
        a.delete()
        resp = {"msg": "加入成功！"}
        return HttpResponse(json.dumps(resp), content_type="application/json")

def test(request):
    return render(request, "test.html", context={})