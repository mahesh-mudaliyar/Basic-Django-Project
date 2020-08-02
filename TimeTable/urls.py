"""TimeTable URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from TimeTableApp import views
urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', views.index),
    path('chkusrname/', views.chkusrname),
    path('registerForm/', views.registerForm),
    path('loginForm/', views.loginForm),
    path('signout/', views.signout),
    path('success/', views.success),
    path('savedata/', views.savedata),
    path('loadata/', views.loadata),
    path('deldata/', views.deldata),
    path('ajax-dropdown/', views.ajaxdropdown),

]
