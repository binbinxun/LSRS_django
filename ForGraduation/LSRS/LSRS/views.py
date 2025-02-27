
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.forms import authenticate
from django.contrib import messages
from django.contrib.auth import login, logout

from django.db import transaction
import datetime
from django.utils import timezone
from django.http import HttpResponse

from . import settings
from .forms import ReservationForm
from .models import Users,Reservations,Seats
import logging
logger = logging.getLogger('LSRS.reservations')  # 获取专用日志器

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('mine')  # 登录成功后跳转到主页（可以根据需要修改）
        else:
            messages.error(request, "Invalid username or password")

    return render(request, 'LSRS/login.html')
def home_redirect(request):
    return redirect('LSRS/login')
@login_required(login_url='/LSRS/login/')
def current_datetime(request):
    now = timezone.now()
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
        created_at= timezone.now()
        u=Users(username=username,password=password,phone=phone,created_at=created_at,is_active=True)
        u.set_password(password)
        u.save()
        return redirect("login")
    return render(request, 'LSRS/register.html')
@login_required(login_url='/LSRS/login/')
def profile_view(request):
    if request.user.is_authenticated:
        reservations = Reservations.objects.filter(user=request.user,status='reserved' or 'confirmed')
        return render(request,'LSRS/mine.html', {'reservations': reservations})
    return redirect('LSRS/login')

@login_required(login_url='/LSRS/login/')
def logout_view(request):
    logout(request)
    return redirect( 'login')  # 默认跳转到首页


def settings_view():
    return None


def message():
    return None

holidays = [
    timezone.make_aware( datetime.datetime(2025, 1, 1)),  # 元旦
    timezone.make_aware( datetime.datetime(2025, 2, 14))  # 情人节
    # 其他节假日
]

from django.utils import timezone
@login_required
def reserve_seat(request):
    error_message = None
    available_seats = Seats.objects.filter(status='available')
    min_start_time = timezone.now().strftime("%Y-%m-%dT%H:%M")  # 使用 Django 时区
    base_time = timezone.localtime(timezone.now()).replace(hour=8, minute=0)  # 当日08:00基准[^5]
    max_end_day = base_time + datetime.timedelta(hours=14)  # 22:00截止

    if settings.MAX_DURATION_MODE == 0:
        max_duration = datetime.timedelta(minutes=30)  # 最短30分钟[^4]
        max_end = timezone.now() + max_duration
    else:
        max_end = max_end_day  # 不限制时长
    if request.method != 'POST':
        return render(request, 'LSRS/reserve.html', {
            'available_seats': available_seats,
            'min_start_time': min_start_time
        })

    seat_id = request.POST.get('seat_id')
    raw_start = request.POST.get('start_time')
    raw_end = request.POST.get('end_time')

    try:
        # 时间转换（关键修复部分）
        naive_start = datetime.datetime.fromisoformat(raw_start)
        naive_end = datetime.datetime.fromisoformat(raw_end)
        start_time = timezone.make_aware(naive_start)
        end_time = timezone.make_aware(naive_end)
        # 当日时间窗口验证
        if not (base_time <= start_time <= max_end_day):
            raise ValueError("必须在08:00-22:00之间选择")

        # 最短时长验证
        if (end_time - start_time) < datetime.timedelta(minutes=30):
            raise ValueError("预约时长不能少于30分钟")
    except ValueError:
        return render(request, 'LSRS/reserve.html', {
            'error_message': '时间格式无效',
            'available_seats': available_seats,
            'min_start_time': min_start_time
        })

    # 时间校验逻辑
    current_time = timezone.now()
    if start_time < current_time:
        error_message = "开始时间不能早于当前时间"
    elif end_time <= start_time:
        error_message = "结束时间必须晚于开始时间"
    elif any(holiday.date() == start_time.date() for holiday in holidays):
        error_message = "节假日不可预约"

    if error_message:
        return render(request, 'LSRS/reserve.html', {
            'error_message': error_message,
            'available_seats': available_seats,
            'min_start_time': min_start_time
        })

    try:
        with transaction.atomic():
            # 锁定座位记录（关键修改）
            seat = Seats.objects.select_for_update().get(
                seat_id=seat_id,
                status='available'
            )

            # 时间冲突检测（在事务内）
            has_conflict = Reservations.objects.filter(
                seat=seat,
                start_time__lt=end_time,
                end_time__gt=start_time
            ).exists()

            if has_conflict:
                raise ValueError("该时间段内座位已被预约")

            # 创建预约记录
            reservation = Reservations.objects.create(
                user=request.user,
                seat=seat,
                start_time=start_time,
                end_time=end_time,
                status='reserved'
            )

            # 更新座位状态
            seat.status = 'occupied'
            seat.save()

            return redirect('reservation_success')

    except Seats.DoesNotExist:
        error_message = "该座位已被占用"
    except ValueError as ve:
        error_message = str(ve)


    return render(request, 'LSRS/reserve.html', context={'error_message': error_message, 'available_seats': available_seats, 'min_start_time': min_start_time})




def reservation_success(request):
    return render(request, 'LSRS/reserve_success.html')


def time_select(request):
    # 设置当日基准时间为08:00
    base_time = timezone.localtime(timezone.now()).replace(hour=8, minute=0, second=0)  # [^2]
    # 设置最大截止时间为22:00
    max_end_day = base_time.replace(hour=22, minute=0)

    # 对齐到最近的10分钟粒度（如09:07→09:10）
    now_aligned = timezone.localtime(timezone.now()).replace(
        minute=10 * (timezone.localtime(timezone.now()).minute // 10)
    )  # [^4]

    return render(request, 'time_select.html', {
        'min_start': base_time.strftime('%Y-%m-%dT%H:%M'),
        'max_end': max_end_day.strftime('%Y-%m-%dT%H:%M'),
        'now_aligned': now_aligned.strftime('%Y-%m-%dT%H:%M')  # 当前对齐时间
    })
