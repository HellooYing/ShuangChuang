#encoding: utf-8
from django.db import models
class village(models.Model):
    village40 = models.CharField('village40',max_length = 5000,default = ' ' )
    postoffice = models.CharField('postoffice',max_length = 500,default = ' ' )
    shortest = models.CharField('shortest',max_length = 500,default = ' ' )
# Create your models here.
