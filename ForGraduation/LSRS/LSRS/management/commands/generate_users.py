from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from LSRS.models import Users
from django.utils import timezone
from faker import Faker
import random


class Command(BaseCommand):
    help = '生成测试用户数据 [参数: --count=10]'

    def add_arguments(self, parser):
        parser.add_argument('--count', type=int, default=10)

    def handle(self, *args, **options):
        fake = Faker('zh_CN')
        base_username = "testuser_"

        for i in range(1, options['count'] + 1):
            Users.objects.create(
                username=f"{base_username}{i}",
                phone=f"1{random.randint(30, 99)}{fake.numerify(text='#######')}",
                created_at=timezone.make_aware(fake.date_time_this_year()),
                password=make_password("123456")  # 使用哈希密码存储
            )
        self.stdout.write(self.style.SUCCESS(f'成功生成{options["count"]}个测试用户'))
