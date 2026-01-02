from pydantic import BaseModel, Field
from typing import Optional

#
from src.domain.enums import AudioQuality, Platforms


class DTO_GetIframe(BaseModel):
    url: str = Field(min_length=1, max_length=2083)
    platform: Platforms = Platforms.YOUTUBE


class DTO_Download(BaseModel):
    url: str = Field(min_length=1, max_length=2083)
    title: Optional[str] = Field(None, min_length=1, max_length=64)
    platform: Platforms = Platforms.YOUTUBE


class DTO_AudioDownload(DTO_Download):
    # quality: AudioQuality = AudioQuality.HIGH
    pass


class DTO_VideoDownload(DTO_Download):
    pass
