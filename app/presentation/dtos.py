from pydantic import BaseModel, Field
from typing import Optional

#
from shared.literals import Platforms, DownloadMode


class DTO_GetIframe(BaseModel):
    url: str = Field(min_length=1, max_length=2083)
    platform: Platforms = "youtube"


class DTO_Download(BaseModel):
    url: str = Field(min_length=1, max_length=2083)
    title: Optional[str] = Field(None, min_length=1, max_length=64)
    platform: Platforms = "youtube"
    mode: DownloadMode = "audio"
