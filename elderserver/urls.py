"""elderserver URL Configuration

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
from django.urls import path, include
from django.views import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static as urls_static
from django.conf.urls import url
from giver import views

urlpatterns = [
    url(r'^(?P<template>[0-9]{1})', views.homepage),
    path('', views.homepage, name='homepage'),
    path('thanks/', views.thanks, name='thanks'),
    path('face/', views.face, name='face'),
    path('navigation', views.navigation, name='navigation'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('care/editshift', views.edit_shift, name='editshift'),
    path('care/shifts', views.shifts, name='shifts'),
    path('care/', include('giver.urls')),
    path('static/', static.serve, {'document_root': settings.STATIC_ROOT}),
    path('admin/', admin.site.urls),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += urls_static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
