from apscheduler.schedulers.background import BackgroundScheduler
from django.utils.timezone import now
import os
import sys
import django
from datetime import datetime

# 1. 添加项目根目录到 Python 路径
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)

# 2. 设置 Django 环境变量，确保可以正确加载 settings.py 配置
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LSRS.settings')

# 3. 初始化 Django 环境，这样就可以访问模型和其他 Django 配置
django.setup()

# 导入模型
from LSRS.models import Reservations, Seats

def update_expired_reservations():
    """
    查找所有已过期的预约，并更新其状态和相关座位的状态
    """
    current_time = datetime.now()  # 获取当前时间
    expired_reservations = Reservations.objects.filter(end_time__lt=current_time, status='confirmed')

    # 更新过期的预约和座位
    for reservation in expired_reservations:
        reservation.status = 'expired'  # 将预约状态更新为过期
        reservation.save()

        seat = reservation.seat  # 获取相关座位
        seat.status = 'available'  # 将座位状态更新为可用
        seat.save()

    print(f"Updated {expired_reservations.count()} expired reservations and their seats.")

def start_scheduler():
    """
    启动 APScheduler 定时任务
    """
    scheduler = BackgroundScheduler()
    # 每隔一分钟检查一次过期预约
    scheduler.add_job(update_expired_reservations, 'interval', minutes=1)
    scheduler.start()

    try:
        while True:
            pass  # 保持任务运行，直到遇到停止信号
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()  # 处理停止信号，优雅地关闭任务

if __name__ == "__main__":
    # 启动定时任务
    start_scheduler()
