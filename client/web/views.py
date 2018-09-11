from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponse
import os
import json
from web.models import Feature, Tracking, Sum
from datetime import datetime

def index(request):
    car_feature = Feature.objects.filter().order_by('-id')[:6]
    for i in car_feature:
        i.time=i.time.split("^")[-1]
        i.time=i.time[-4:-2]+":"+i.time[-2:-1]+i.time[-1]
        i.location=i.location.split("^")[-1]
        print(type(i.kind))
        if i.kind=="0":
            i.kind="油罐车"
        elif i.kind=="1":
            i.kind="大货车"
        elif i.kind=="4":
            i.kind="大客车"
    car_tracking = Tracking.objects.filter().order_by('-id')[:6]
    all_car = Sum.objects.filter()[0:1]
    return render(request, "index.html", context={'car_feature': car_feature,'car_tracking':car_tracking,'all_car':all_car})

def tracking(request):
    all_car = Tracking.objects.all()
    return render(request, "tracking.html", context={'all_car': all_car})


def change_route(request):
    num = request.GET.get('num')
    car = Tracking.objects.filter(number=num)
    location = []
    time = []
    for i in car:
        location = i.location.split('^')
        time = i.time.split("^")
    response_data = {'location': location, 'time': time}
    return HttpResponse(json.dumps(response_data), content_type="application/json")

def new(request):
    b=Tracking()
    b.number = request.GET.get("number")#这个是车牌号,在收费口是可以判别的
    b.time = request.GET.get("time")
    b.location = request.GET.get("location")
    b.color = request.GET.get("color")
    b.kind = request.GET.get("kind")
    b.save()
    a=Feature()
    a.number = b.id
    a.time = request.GET.get("time")
    a.location = request.GET.get("location")
    a.color = request.GET.get("color")
    a.kind = request.GET.get("kind")
    a.save()
    
    c=Sum()
    c.total=1
    if int(request.GET.get("kind"))==1:
        c.car1=1
    elif int(request.GET.get("kind"))==2:
        c.car2=1
    elif int(request.GET.get("kind"))==3:
        c.car3=1
    elif int(request.GET.get("kind"))==4:
        c.car4=1
    else:
        resp={"msg": "车型出错！"}
        return HttpResponse(json.dumps(resp), content_type="application/json")
    c.save()
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
        b = Tracking.objects.get(id=a.number)
        b.location = b.location+"^"+location
        b.time = b.time+"^"+time
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