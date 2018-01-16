#encoding: utf-8
from django.db import models
class Car(models.Model):
    plate_number = models.CharField('plate_number',max_length = 50,default = ' ',primary_key=True )
    point = models.TextField('point',default = ' ' )
    point_time = models.TextField('point_time',default = ' ' )
# Create your models here.
