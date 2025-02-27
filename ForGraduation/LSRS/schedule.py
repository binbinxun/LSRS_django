# LSRS/scheduler.py
import sys
import os
import logging
from datetime import datetime

from apscheduler.schedulers.blocking import BlockingScheduler
from django.core.management import call_command

# ---------- 环境初始化 ----------
# 配置项目路径（根据实际路径调整）
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

# 设置 Django 环境变量
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "LSRS.settings")
print(BASE_DIR)
# 初始化 Django
import django

django.setup()

# ---------- 日志配置 ----------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


# ---------- 定时任务 ----------
def job():
    try:
        logger.info("开始执行自动释放任务")
        call_command("expirereservations")  # 调用你的管理命令
        logger.info("任务执行完成")
    except Exception as e:
        logger.error(f"任务执行失败: {str(e)}", exc_info=True)


if __name__ == "__main__":
    scheduler = BlockingScheduler()

    # 每 60 秒执行一次（立即执行第一次）
    scheduler.add_job(job, "interval", seconds=60, next_run_time=datetime.now())

    try:
        logger.info("定时任务服务已启动")
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        logger.info("正在关闭定时任务...")
        scheduler.shutdown()
        logger.info("服务已关闭")