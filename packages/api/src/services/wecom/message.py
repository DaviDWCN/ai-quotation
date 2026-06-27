from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class WeComMessageType(str, Enum):
    TEXT = "text"
    IMAGE = "image"
    FILE = "file"


class WeComBaseMessage(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    to_user_name: str = Field(alias="ToUserName")
    from_user_name: str = Field(alias="FromUserName")
    create_time: int = Field(alias="CreateTime")
    msg_type: WeComMessageType = Field(alias="MsgType")
    msg_id: str = Field(alias="MsgId")


class WeComTextMessage(WeComBaseMessage):
    content: str = Field(alias="Content")


class WeComImageMessage(WeComBaseMessage):
    pic_url: str = Field(alias="PicUrl")
    media_id: str = Field(alias="MediaId")


class WeComFileMessage(WeComBaseMessage):
    file_name: str = Field(alias="FileName")
    file_ext: str = Field(alias="FileExt")
    media_id: str = Field(alias="MediaId")
    file_size: int = Field(alias="FileSize")
