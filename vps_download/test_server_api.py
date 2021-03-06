import os

from data_type import FileListForm
from server_api import ServerAPI


def test_server_api():
    token = os.environ.get("APP_KEY")
    api = ServerAPI()
    form = FileListForm(token=token)
    ret = api.get_job_list(form)
    assert ret is not None
    assert len(ret) != 0
