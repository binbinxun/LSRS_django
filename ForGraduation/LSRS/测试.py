import datetime
from django.utils import timezone

print(timezone)  # 查看实际引用的是哪个对象
now = timezone.now()  # 正常获取当前时间
