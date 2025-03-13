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
    path("mine",views.profile_view,name="mine"),
    path("settings",views.settings_view,name="settings"),
    path("message",views.message,name="messages"),
    path("logout",views.logout_view,name="logout"),
    path('reserve/', views.reserve_seat, name='reserve_seat'),  # 添加预约页面的 URL 路由
    path('reservation_success/', views.reservation_success, name='reservation_success'),
    path('check_in',views.check_in,name='check_in'),
    path('seat_map', views.reserve_map, name='seat_map'),
    path("api/seat_detail/<int:seat_id>",
         views.seat_detail_api,
        name="seat_detail_api"),
    path('reserve_cancel',views.reserve_cancel,name='reserve_cancel')
]
