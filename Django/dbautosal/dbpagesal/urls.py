from django.urls import path
from django.conf.urls import url,include
from django.contrib.auth import views as auth_viewsfrom .import views

app_name = "dbpagesal"
#print("y")
urlpatterns = [
#     path('', views.index, name='login'),
    url(r'^index/$',views.index,name="index"), 
    url(r'^verify/$',views.verify,name="verify"), 
    url(r'^info/$',views.info,name="info"),
    url(r'^detail/$',views.detail,name="detail"),
    url(r'^complete/$',views.complete,name="complete"),
]