#encoding: utf-8
from django.db import models
class Car(models.Model):
    plate_number = models.CharField('plate_number',max_length = 50,default = ' ',primary_key=True )
    point = models.TextField('point',default = ' ' )
    point_time = models.TextField('point_time',default = ' ' )

class Feature(models.Model):
    number = models.CharField('编号',max_length = 150)
    time = models.CharField('时间',max_length = 150)
    location = models.CharField('树莓派',max_length = 150)
    color = models.CharField('颜色',max_length = 50,default = '')
    kind = models.CharField('类型细化',max_length = 50,default = '')
    def __str__(self):
        return self.id


class Tracking(models.Model):
    number = models.CharField('编号',max_length = 150)#保留第一个
    time = models.CharField('时间',max_length = 150)#保留全部，是一个被转化为字符串存储的字符串数组
    location = models.CharField('树莓派',max_length = 150)#保留全部，与time一一对应
    def __str__(self):
        return self.id
