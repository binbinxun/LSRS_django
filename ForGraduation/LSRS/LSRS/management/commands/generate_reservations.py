# management/commands/generate_reservations.py
# python manage.py batch_reservations

from django.core.management.base import BaseCommand
from django.db import transaction
from LSRS.models import Reservations, Seats, Users
import random
from django.utils import timezone
from datetime import timedelta


class Command(BaseCommand):
    help = '批量生成不冲突预约记录'

    def handle(self, *args, **options):
        users = Users.objects.all()[:20]  # 获取前20个用户
        seats = Seats.objects.filter(status='available')[:50]  # 获取可用座位

        base_time = timezone.now().replace(minute=0, second=0, microsecond=0)

        with transaction.atomic():
            for seat in seats.select_for_update():  # 行级锁保障并发安全
                time_slot = base_time

                for user in random.sample(list(users), 3):  # 每个座位分配3个用户
                    start_time = base_time + timedelta(hours=random.randint(1, 48))
                    end_time = start_time + timedelta(hours=random.randint(1,10))

                    # 冲突检测逻辑
                    if not Reservations.objects.filter(
                            seat=seat,
                            start_time__lt=end_time,
                            end_time__gt=start_time
                    ).exists():
                        Reservations.objects.create(
                            user=user,
                            seat=seat,
                            reservation_time=timezone.now(),  # 使用模型定义字段
                            start_time=start_time,
                            end_time=end_time,
                            status='reserved'
                        )
                        time_slot = end_time + timedelta(hours=1)  # 间隔1小时
