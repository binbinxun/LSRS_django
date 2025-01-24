from django.urls import path

from . import views
namespace="lsrs2"
urlpatterns = [
    path("", views.index, name="index"),
]