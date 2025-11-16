from fastapi import APIRouter

#
from src.application.responses import Respuesta
from src.application.use_cases.get_audio_iframe import UC_GetAudioIframe
from src.application.use_cases.download_audio import UC_AudioDownload
from src.presentation.dtos import (
    DTO_GetAudioIframe,
    DTO_AudioDownload,
    DTO_VideoDownload,
)
from src.application.use_cases.download_video import UC_VideoDownload


router = APIRouter()


@router.post("/get_audio_iframe/")
async def get_audio_iframe(dto: DTO_GetAudioIframe) -> Respuesta:
    result = await UC_GetAudioIframe(url=dto.url, platform=dto.platform.value).execute()
    return result


@router.post("/download_audio/")
async def download_audio(dto: DTO_AudioDownload):
    result = await UC_AudioDownload(
        url=dto.url,
        title=dto.title,
        platform=dto.platform.value,
        quality=dto.quality.value,
    ).execute()
    return result


@router.post("/download_video/")
async def download_video(dto: DTO_VideoDownload):
    result = await UC_VideoDownload(
        url=dto.url,
        title=dto.title,
        platform=dto.platform.value,
        quality=dto.quality.value,
    ).execute()
    return result
