from django.contrib import admin
from web import models

admin.site.register(models.Tracking)

#将版社注册到admin后台
admin.site.register(models.Feature)
