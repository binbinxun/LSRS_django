
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import authenticate
from django.contrib import messages
from django.contrib.auth import login, logout
from django.conf.global_settings import TIME_ZONE
from django.db import transaction, IntegrityError
import datetime
from django.utils import timezone
from django.http import HttpResponse, JsonResponse
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
# views.py
from django.db import DatabaseError
from django.views.decorators.http import require_http_methods
from datetime import timedelta
import datetime

@login_required
@require_http_methods(["GET", "POST"])
def reserve_seat(request):
    # 公共上下文数据
    context = {
        "available_seats": Seats.objects.filter(status="available"),
        "min_start_time": _calculate_min_start_time(),
        "max_end_time": _calculate_max_end_time()
    }

    if request.method == "GET":
        return render(request, "LSRS/reserve.html", context)

    # POST处理流程
    try:
        # 基础验证
        seat_id = request.POST.get("seat_id")
        raw_start = request.POST.get("start_time")
        raw_end = request.POST.get("end_time")

        # 转换时区感知时间
        start_time = timezone.make_aware(
            datetime.datetime.fromisoformat(raw_start)
        )
        end_time = timezone.make_aware(
            datetime.datetime.fromisoformat(raw_end)
        )

        # 基本验证
        if start_time >= end_time:
            raise ValueError("结束时间必须晚于开始时间")
        if (end_time - start_time) < timedelta(minutes=30):
            raise ValueError("预约时长不能少于30分钟")
        if start_time < timezone.now():
            raise ValueError("不能预约过去的时间")

        # 执行预约
        with transaction.atomic():
            # 锁定座位
            try:
                seat = Seats.objects.select_for_update(
                    nowait=True
                ).get(
                    seat_id=seat_id,
                    status="available"
                )
            except Seats.DoesNotExist:
                raise ValueError("座位不存在或不可用")
            except DatabaseError:
                raise ValueError("当前预约人数过多，请稍后重试")

            # 检查时间冲突
            if Reservations.objects.filter(
                seat=seat,
                start_time__lt=end_time,
                end_time__gt=start_time
            ).exists():
                raise ValueError("该时间段已被预约")

            # 检查节假日
            # if Holidays.objects.filter(date=start_time.date()).exists():
            #     raise ValueError("节假日不可预约")

            # 创建预约
            reservation = Reservations.objects.create(
                user=request.user,
                seat=seat,
                start_time=start_time,
                end_time=end_time,
                status="reserved"
            )

            return render(request, "LSRS/reserve_success.html",
                        {"reservation": reservation})

    except (ValueError, DatabaseError) as e:
        context["error_message"] = str(e)
        return render(request, "LSRS/reserve.html", context)

def _calculate_min_start_time():
    """计算最早可预约时间"""
    now = timezone.localtime(timezone.now())
    minutes_to_add = (10 - now.minute % 10) % 10
    return (now + timedelta(minutes=minutes_to_add)).replace(
        second=0, microsecond=0
    )

def _calculate_max_end_time():
    """计算最晚结束时间"""
    base = timezone.localtime(timezone.now()).replace(
        hour=8, minute=0, second=0
    )
    return base + timedelta(hours=14)

@login_required()
def reservation_success(request):
    return render(request, 'LSRS/reserve_success.html')

@login_required()
def check_in(request):
    if request.method == 'GET':
        # 获取当前登录用户的预约记录，筛选出 status 为 "reserved" 且 checked_in 为 0 的记录
        rsvtions = Reservations.objects.filter(user=request.user, status="reserved", checked_in=0)
        return render(request, "LSRS/check_in.html", context={'reservations': rsvtions})

    if request.method == 'POST':
        # 处理签到逻辑
        rsv_id = request.POST.get('rsv_id')
        try:
            reservation = Reservations.objects.get(reservation_id=rsv_id)
            if reservation.status == 'reserved' and reservation.checked_in == 0 and (timezone.now()-reservation.start_time).total_seconds()<30*60:
                # 进行签到操作
                reservation.checked_in = 1
                reservation.check_in_time=timezone.now()
                reservation.save()
                # 提示用户签到成功
                return redirect('check_in')
            else:
                if (timezone.now()-reservation.start_time).total_seconds()>30*60:
                    return render(request,context={'error_message':"请于当天开始时间半小时左右签到"})


                # 如果状态不是 reserved 或已经签到，返回错误页面
                return redirect('check_in')  # 或者其他提示信息页面
        except Reservations.DoesNotExist:
            # 如果找不到该预约记录，返回错误页面或者跳转到其他页面
            return redirect('check_in')  # 或者其他提示信息页面

    return redirect('mine')


def time_select(request):
    # 设置当日基准时间为08:00
    base_time = timezone.localtime(timezone.now()).replace(hour=8, minute=0, second=0)  #
    # 设置最大截止时间为22:00
    max_end_day = base_time.replace(hour=22, minute=0)

    # 对齐到最近的10分钟粒度（如09:07→09:10）
    now_aligned = timezone.localtime(timezone.now()).replace(
        minute=10 * (timezone.localtime(timezone.now()).minute // 10)
    )

    return render(request, 'time_select.html', {
        'min_start': base_time.strftime('%Y-%m-%dT%H:%M'),
        'max_end': max_end_day.strftime('%Y-%m-%dT%H:%M'),
        'now_aligned': now_aligned.strftime('%Y-%m-%dT%H:%M')  # 当前对齐时间
    })

@login_required()
def reserve_cancel(request):
    reservations = Reservations.objects.filter(user=request.user, status='reserved' or 'confirmed')
    if request.method!="POST":
        return render(request,"LSRS/reserve_cancel.html",context={
            'rsvs':reservations
        })
    message = None  # 初始化消息变量
    #rid=None
    # 第一部分：获取 reserve_id
    try:
        # 使用[]直接获取，若键不存在会引发KeyError
        rid = request.POST.get('reserve_id')
        print(rid)
    except KeyError:
        message = "错误：未提供预约ID参数"
    except AttributeError:
        # 若request没有POST属性（如非POST请求）
        message = "错误：请求格式不正确"
    except Exception as e:
        # 其他未知错误（如request对象异常）
        message = f"获取预约信息失败：{str(e)}"
    else:
        # 第二部分：查询数据库（仅在rid获取成功时执行）
        try:
            rsv = Reservations.objects.get(reservation_id=rid)
        except Reservations.DoesNotExist:
            message = "错误：指定的预约不存在"
        except ValueError:
            message = "错误：预约ID格式无效"
        except Exception as e:
            message = f"查询预约时发生未知错误：{str(e)}"
        else:
            # 成功获取rsv对象，继续后续业务逻辑
            with transaction.atomic():
                rsv.status='canceled'

                rsv.save()
            message="已取消预约"
    print(f"rid类型: {type(rid)}, 值: {rid}")
    print("传递的rsvs数量:", len(reservations))  # 在视图中添加调试输出
    print("message内容:", message)
    return render(request,"LSRS/reserve_cancel.html",context={
        'rsvs':reservations,
        'message':message
    })

def parse_time(iso_str: str) -> datetime:
    try:
        dt = datetime.datetime.fromisoformat(iso_str)
        dt=timezone.make_aware(dt)
        if dt < timezone.now():
            raise ValueError("不能选择过去时间")
        return dt
    except ValueError:
        raise ValueError("非法时间格式")
@login_required
def reserve_map(request):
    """座位地图可视化核心视图"""
    seats = Seats.objects.all().prefetch_related('reservations')
    base_time = timezone.now().replace(hour=8, minute=0, second=0)
    if request.method=='POST':
        logger.debug(f"Received POST data: {request.POST}")  # 检查 POST 数据
        logger.debug(f"Request body: {request.body}")  # 检查原始请求体
        seat_id = request.POST.get('seat_id')
        if seat_id==None:
            return JsonResponse({
                'error':'提交座位号失败'
            })
        seat = Seats.objects.get(seat_id=int(seat_id))
        start_time = parse_time(request.POST.get('start_time'))
        end_time = parse_time(request.POST.get('end_time'))
        with transaction.atomic():
            try:
                if Reservations.objects.filter(
                        seat=seat,
                        end_time__gt=start_time,
                        start_time__lt=end_time,
                        status='reserved'
                ).exists():
                    return JsonResponse({
                        'error': '时间段冲突'
                    })
                Reservations.objects.create(
                    user=request.user,
                    seat=seat,
                    start_time=start_time,
                    end_time=end_time
                )
            except Seats.DoesNotExist as e:
                return JsonResponse({
                    'error': '座位不存在'+str(e)
                })
            except Exception as e:
                print(e)
                print('数据保存失败')
                return JsonResponse({
                    'error': '数据保存失败'+str(e)
                })

            else:
                return JsonResponse({
                    'success':1
                })

    return render(request, 'LSRS/reserve_map.html', {
        'seats': seats,
        'time_step': 30,  # 时间选择步长参数化
        'base_time': base_time.strftime('%Y-%m-%dT%H:%M')
    })
# def seat_status_api(request):
#     """实时座位状态API"""
#     timestamp = request.GET.get('timestamp')
#     seats_data = {
#         seat.seat_id: seat.current_status()
#         for seat in Seats.objects.all()
#     }
#     return JsonResponse(seats_data)


def seat_detail_api(request, seat_id):

    try:
        seat = Seats.objects.get(seat_id=seat_id)
    except Exception as e:
        logger.error(str(e))
        return JsonResponse({"error_message" : str(e)})

    else:
        # 过滤未过期且状态有效的预约
        reservations = seat.reservations.filter(
            end_time__gte=timezone.now(),
            status="reserved"
        ).values("start_time", "end_time")

        return JsonResponse({
            'error_message':"没出错",
            "min_start": timezone.now().isoformat(),
            "max_end": _calculate_max_end_time(),  # 时间计算逻辑 [^5]
            "reservations": list(reservations)
        })

