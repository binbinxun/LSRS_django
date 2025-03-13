from random import random

from django.core.management import BaseCommand

from ForGraduation.LSRS.LSRS.models import Seats


class Command(BaseCommand):
    def handle(self, *args, **options):
        # 示例生成逻辑
        for i in range(1, 100):
            Seats.objects.create(
                seat_id=f"A-{i}",
                x_pos=random.randint(50, 750),  # 随机X坐标[^2]
                y_pos=random.randint(50, 550),  # 随机Y坐标
                has_power=(i % 5 == 0)
            )
