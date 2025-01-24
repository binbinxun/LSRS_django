from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.forms import authenticate
from django.contrib import messages
from django.contrib.auth import login

import datetime
from django.http import HttpResponse

from .models import Users


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('ct')  # 登录成功后跳转到主页（可以根据需要修改）
        else:
            messages.error(request, "Invalid username or password")

    return render(request, 'LSRS/login.html')
def home_redirect(request):
    return redirect('LSRS/login')
@login_required(login_url='/LSRS/login/')
def current_datetime(request):
    now = datetime.datetime.now()
    html = '<html lang="en"><body>It is now %s.</body></html>' % now
    return HttpResponse(html)

@login_required(login_url='/LSRS/login/')
def home(request):
    return HttpResponse("Welcome to the Library Seat Reservation System!")

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        phone=request.POST.get("phone")
        created_at= datetime.datetime.now()
        u=Users(username=username,password=password,phone=phone,created_at=created_at)
        u.set_password(password)
        u.save()
        return redirect("login")
    return render(request, 'LSRS/register.html')