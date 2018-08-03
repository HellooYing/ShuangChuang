from django.conf.urls import url
from . import views
app_name = 'web'
urlpatterns = [
    url(r'^$',views.index,name='index'),
    url(r'^upload',views.upload,name='upload'),
    url(r'^test',views.test,name='test'),
    url(r'^new',views.new,name='new'),
    url(r'^change_route',views.change_route,name='change_route'),
]
