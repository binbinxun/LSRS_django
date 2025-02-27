from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone
from LSRS.models import Reservations, Seats
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = '自动释放过期座位（优化版）'

    def handle(self, *args, **options):
        try:
            with transaction.atomic():  # 启用事务
                # 1. 锁定并获取过期预约
                expired = Reservations.objects.select_for_update().filter(
                    end_time__lt=timezone.now(),
                    status='reserved'
                )

                # 2. 批量更新预约状态
                updated_reservations = expired.update(status='expired')

                # 3. 获取关联座位ID（去重）
                seat_ids = expired.values_list('seat_id', flat=True).distinct()

                # 4. 批量更新座位状态
                updated_seats = Seats.objects.filter(
                    seat_id__in=seat_ids
                ).update(status='available')

                # 5. 记录日志
                logger.info(
                    f"处理成功 | 更新预约: {updated_reservations} 条, "
                    f"释放座位: {updated_seats} 个"
                )
                self.stdout.write(
                    self.style.SUCCESS(f"成功处理 {updated_reservations} 条预约")
                )

        except Exception as e:
            logger.error(f"处理失败: {str(e)}", exc_info=True)
            self.stdout.write(self.style.ERROR('处理过程中发生错误'))