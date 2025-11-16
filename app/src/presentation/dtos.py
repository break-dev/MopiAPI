from pydantic import BaseModel, Field
from typing import Optional

#
from src.domain.classes import AudioPlatforms, AudioQuality

class DTO_GetAudioIframe(BaseModel):
    url: str = Field(min_length=1, max_length=2048)
    platform: AudioPlatforms = AudioPlatforms.YOUTUBE

class DTO_AudioDownload(BaseModel):
    url: str = Field(min_length=1, max_length=2048)
    title: Optional[str] = Field(None, min_length=1, max_length=64)
    platform: AudioPlatforms = AudioPlatforms.YOUTUBE
    quality: AudioQuality = AudioQuality.MEDIUM


