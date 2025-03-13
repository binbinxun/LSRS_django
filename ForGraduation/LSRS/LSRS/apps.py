# apps.py 增加现代Django必须的配置项
from django.apps import AppConfig


class LSRSConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'  # 现代Django必须字段
    name = "LSRS"
    label = 'LSRS'

    # 取消ready方法的注释以激活信号
    def ready(self):
        import signal # 确保信号系统正常工作
