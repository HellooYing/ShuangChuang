from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$',views.index,name='index'),
    url(r'^test',views.test,name='test'),
    url(r'^change_route',views.change_route,name='change_route'),
]
