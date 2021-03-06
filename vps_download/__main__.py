import os
import sys
from typing import Optional

import click
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger

from do_once import do_run_once


def run_once(app_key: str):
    do_run_once(app_key)


def real_main(app_key: str):
    def do_job():
        run_once(app_key)

    scheduler = BlockingScheduler()
    trigger = CronTrigger(hour=0, minute=0)
    scheduler.add_job(do_job, trigger)
    scheduler.start()


@click.command()
@click.option(
    "--app-key", type=str, default=lambda: os.environ.get("APP_KEY", None), help="服务器令牌"
)
@click.option("--once", is_flag=True, type=bool, help="只允许一次, 还是作为守护进程运行")
def main(app_key: Optional[str], once: bool):
    """
    下载文件测试
    """
    if app_key is None:
        print(f"app-key 没有设置")
        sys.exit(1)

    if once:
        run_once(app_key)
    else:
        real_main(app_key)


if __name__ == "__main__":
    main()
