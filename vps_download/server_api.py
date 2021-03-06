import logging
from typing import List

import requests

from data_type import FileListForm, FileReportForm, FileItem, FileListResp

__all__ = ["ServerAPI"]


class ServerAPI(object):
    """
    服务器 API
    """

    def __init__(self):
        self._session = requests.Session()
        self._url = "https://vps.qiyutech.tech/api/monitor/file"

    def report(self, form: FileReportForm) -> bool:
        try:
            url = f"{self._url}/report"
            ret = self._session.post(url, json=form.dict(), timeout=(5, 5))
            return ret.ok
        except Exception as e:
            print(f"catch exception: {e}")
            return False

    def get_job_list(self, form: FileListForm) -> List[FileItem]:
        try:
            url = f"{self._url}/list"
            ret = self._session.post(url, json=form.dict(), timeout=(5, 5))
            if not ret.ok:
                logging.error(f"get job list {ret=}")
                return []
            data = FileListResp(**ret.json())
            return data.data_list
        except Exception as e:
            logging.error(f"catch exception: {e}")
            return []
