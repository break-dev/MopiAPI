from pydantic import BaseModel, Field
from typing import Optional

#
from src.domain.enums import (
    AudioPlatforms,
    AudioQuality,
    VideoPlatforms,
    VideoQuality,
)


class DTO_GetAudioIframe(BaseModel):
    url: str = Field(min_length=1, max_length=2048)
    platform: AudioPlatforms = AudioPlatforms.YOUTUBE


class DTO_GetVideoIframe(BaseModel):
    url: str = Field(min_length=1, max_length=2048)
    platform: VideoPlatforms = VideoPlatforms.YOUTUBE


class DTO_AudioDownload(BaseModel):
    url: str = Field(min_length=1, max_length=2048)
    title: Optional[str] = Field(None, min_length=1, max_length=64)
    platform: AudioPlatforms = AudioPlatforms.YOUTUBE
    quality: AudioQuality = AudioQuality.MEDIUM


class DTO_VideoDownload(BaseModel):
    url: str = Field(min_length=1, max_length=2048)
    title: Optional[str] = Field(None, min_length=1, max_length=64)
    platform: VideoPlatforms = VideoPlatforms.YOUTUBE
    quality: VideoQuality = VideoQuality.MEDIUM
