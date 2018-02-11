"""guest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from sign import views_if, test2, views

app_name='[sign]'
urlpatterns = [
    # sign system interface
    #ex: /api/add_event/
    url(r'^add_event/', views_if.add_event,name='add_event'),
    # ex: /api/add_guest/
    url(r'^add_guest/', views_if.add_guest,name='add_guest'),
    # ex: /api/get_event_list/
    url(r'^get_event_list/', views_if.get_event_list,name='get_event_list'),
    # ex: /api/get_guest_list/
    # url(r'^get_guest_list/', views_if.get_guest__list,name='get_guest_list'),
    # ex: /api/user_sign/
    # url(r'^user_sign/', views_if.user_sign,name='user_sign'),
    url(r'^test/', test2.test,name='test'),


]
