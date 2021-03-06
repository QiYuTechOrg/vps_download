from typing import Optional, List

from pydantic import BaseModel, Field

__all__ = ["FileListForm", "FileReportForm", "FileItem", "FileListResp"]


class FileItem(BaseModel):
    id: int = Field(..., title="ID")
    file_url: str = Field(..., title="下载地址")


class FileListResp(BaseModel):
    data_list: List[FileItem] = Field(..., title="数据列表")


class TokenForm(BaseModel):
    token: str = Field(..., title="访问令牌")


class FileListForm(TokenForm):
    oid: Optional[int] = Field(None, title="偏移")
    limit: int = Field(10, title="获取多少数据")


class FileReportForm(TokenForm):
    src_ip: str = Field(..., title="IP地址", description="下载的IP地址")
    file_url: str = Field(..., title="文件地址", description="下载文件的地址")
    file_size: int = Field(..., title="文件大小", description="下载了多少")
    consume: float = Field(..., title="下载时间", description="单位为:秒")
