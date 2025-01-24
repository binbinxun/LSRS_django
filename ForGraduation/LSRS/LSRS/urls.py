"""LSRS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.contrib.auth.decorators import login_required
from django.urls import include, path
from django.http import HttpResponse
from . import views
# 定义一个简单的主页视图
namespace="LSRS"


urlpatterns = [
    path('',views.home,name="home"),
    path("login/",views.login_view,name="login"),
    path("cd",views.current_datetime,name="ct"),
    path("register",views.register_view,name="register"),
    path("admin",admin.site.urls)
]
