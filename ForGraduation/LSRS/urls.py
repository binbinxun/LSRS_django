from django.contrib import admin
from django.shortcuts import redirect
from django.urls import include, path
def home_redirect(request):
    return redirect('LSRS/login')
urlpatterns = [
    path("lsrs2/", include("lsrs2.urls")),
    path("admin/", admin.site.urls),
    path("LSRS/",include("LSRS.urls")),
    path("polls/",include("polls.urls")),
    path("",home_redirect,name="home")
]