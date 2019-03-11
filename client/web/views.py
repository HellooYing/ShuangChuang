from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponse
import os
import json
from web.models import Feature, Tracking, Sum, H_tracking
from datetime import datetime

def index(request):
    car_feature = Feature.objects.filter().order_by('-id')[:7]
    for i in car_feature:
        i.time=i.time.split("^")[-1]
        i.time=i.time[-4:-2]+":"+i.time[-2:-1]+i.time[-1]
        i.location=i.location.split("^")[-1]
        if i.kind=="0":
            i.kind="油罐车"
        elif i.kind=="1":
            i.kind="大货车"
        elif i.kind=="4":
            i.kind="大客车"
    a = Sum.objects.filter()[0]
    s = Sum.objects.filter()[1:]
    for j in s:
        a.total=a.total+j.total
        a.car1=a.car1+j.car1
        a.car2=a.car2+j.car2
        a.car3=a.car3+j.car3
        j.delete()
    a.save()
    all_car = Sum.objects.filter()[0:1]
    return render(request, "index.html", context={'car_feature': car_feature,'all_car':all_car})

def history(request):
    car_feature = Feature.objects.filter().order_by('-id')
    for i in car_feature:
        i.time=i.time.split("^")[-1]
        i.time=i.time[-4:-2]+":"+i.time[-2:-1]+i.time[-1]
        i.location=i.location.split("^")[-1]
        if i.kind=="0":
            i.kind="油罐车"
        elif i.kind=="1":
            i.kind="大货车"
        elif i.kind=="4":
            i.kind="大客车"
    a = Sum.objects.filter()[0]
    s = Sum.objects.filter()[1:]
    for j in s:
        a.total=a.total+j.total
        a.car1=a.car1+j.car1
        a.car2=a.car2+j.car2
        a.car3=a.car3+j.car3
        j.delete()
    a.save()
    all_car = Sum.objects.filter()[0:1]
    return render(request, "history.html", context={'car_feature': car_feature,'all_car':all_car})

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
    a.number = b.number
    a.time = request.GET.get("time")
    a.location = request.GET.get("location")
    a.color = request.GET.get("color")
    a.kind = request.GET.get("kind")
    a.save()
    
    k=int(request.GET.get("kind"))
    c=Sum()
    c.total=1
    if k==0:#kind=0以及sum.car3是油罐车
        c.car3=1
    elif k==1:#大货
        c.car1=1
    elif k==4:#客车
        c.car2=1
    elif k==2:
        c.car4=1
        c.total=0
    elif k==3:
        c.car4=1
        c.total=0
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
        b = Tracking.objects.get(number=a.number)
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

def leave(request):
    number = request.GET.get("number")#这个是车牌号,在收费口是可以判别的
    time = request.GET.get("time")
    location = request.GET.get("location")
    t = Tracking.objects.filter(number=number)
    t.location = t.location+"^"+location
    t.time = t.time+"^"+time
    f = Feature.objects.filter(number=number)
    #last=t.location.split('^')[-1]
    #查表获取last的可出现域，如果location在可出现域里，就说明轨迹就是这货的
    #如果不在，就查找现在带着这辆车的车牌号的那辆车，可能是他俩超车让轨迹错了。

    #可能还要考虑带着这辆车车牌号的车有没有被别的特征一样的车超车，不过这么考虑下去我不知道这是不是还是一个能解决的问题
    #所以假设特征一样的车互相超车是个比较小概率的事情，多次超车是小概率的平方先忽略了
    #在两客一危车辆这种不是很常见的车辆里，或许做一个新特征比如size，pattern来降低特征相同的概率是比逻辑上解决多次超车问题更好的方案
    
    #继续这两辆车，从后往前找他俩第一个相同的点，把这个点之后的轨迹交换掉，这样轨迹就正确了！
    #如果没找到，就把先下来的这辆车加入等待序列，等冒名顶替它的那辆下道获取到第二辆车的车牌号，
    #找到参与他们超车惑乱轨迹的第三辆车，找他们互相超车的点。如果还有第四辆车，就继续等待序列。。
    #如果真的有必要我再写超车问题的解决，没必要就先不写了，都赶得上leetcode中级题了。
    h=H_tracking()
    h.number = t.number
    h.time = t.time
    h.location = t.location
    h.color = t.color
    h.kind = t.kind
    h.save()
    c=Sum()
    c.total=-1
    k=t.kind
    if k==0:#kind=0以及sum.car3是油罐车
        c.car3=-1
    elif k==1:#大货
        c.car1=-1
    elif k==4:#客车
        c.car2=-1
    c.save()
    t.delete()
    f.delete()

def test(request):
    return render(request, "test.html", context={})