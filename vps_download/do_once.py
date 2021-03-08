import logging
import time

import requests

from data_type import FileListForm, FileItem, FileReportForm
from server_api import ServerAPI

__all__ = ["do_run_once"]

h = requests.get("https://ifconfig.me/ip", timeout=(5, 5))
src_ip = h.text
logging.info(f"{src_ip=}")


def do_run_once(app_key: str):
    api = ServerAPI()

    oid = 0

    logging.info("start do_run_once")
    while True:
        form = FileListForm(oid=oid, token=app_key)
        job_list = api.get_job_list(form)
        if len(job_list) == 0:
            logging.error("no more job")
            break  # no more job or error

        for job in job_list:
            print(f"got job: {job.id=} {job.file_url}")
            oid = max(oid, job.id)

            file_size, consume = do_one_job(job)
            if file_size <= 0:
                continue  # not download file
            form = FileReportForm(
                token=app_key,
                src_ip=src_ip,
                file_url=job.file_url,
                file_size=file_size,
                consume=consume,
            )
            api.report(form)
            print(f"job done: {job.id}")


def do_one_job(item: FileItem) -> [int, float]:
    file_size = 0
    start = time.time()
    try:
        resp = requests.get(item.file_url, stream=True, timeout=(5, 5))
        resp.raise_for_status()
        for chunk in resp.iter_content(chunk_size=128 * 1024):
            file_size += len(chunk)
            if file_size > 100 * 1024 * 1024:  # 最多下载 100MB
                break
            if time.time() - start > 60:  # 最多测试 60s
                break
        return file_size, time.time() - start
    except Exception as e:
        print(f"download {item.file_url} failed: {e}")
        return file_size, time.time() - start
