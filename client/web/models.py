#encoding: utf-8
from django.db import models

class Feature(models.Model):
    number = models.CharField('编号',max_length = 150)
    time = models.CharField('时间',max_length = 150)
    location = models.CharField('树莓派',max_length = 150)
    color = models.CharField('颜色',max_length = 50,default = '')
    kind = models.CharField('类型细化',max_length = 50,default = '')
    def __str__(self):
        a=self.color+self.kind
        return a


class Tracking(models.Model):
    number = models.CharField('编号',max_length = 150)#保留第一个
    time = models.CharField('时间',max_length = 150)#保留全部，是一个被转化为字符串存储的字符串数组
    location = models.CharField('树莓派',max_length = 150)#保留全部，与time一一对应
    color = models.CharField('颜色',max_length = 50,default = '')
    kind = models.CharField('类型细化',max_length = 50,default = '')
    def __str__(self):
        a=self.color+self.kind
        return a

class Sum(models.Model):
    total = models.IntegerField('车总数',default = 0)
    car1 = models.IntegerField('大货车',default = 0)
    car2 = models.IntegerField('客车',default = 0)
    car3 = models.IntegerField('油罐车',default = 0)
    car4 = models.IntegerField('非两客一危车辆',default = 0)