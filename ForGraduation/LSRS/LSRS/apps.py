from django.apps import AppConfig


class LSRSConfig(AppConfig):
    name="LSRS"
    label='LSRS'

    def ready(self):
        #import LSRS.signals
        pass