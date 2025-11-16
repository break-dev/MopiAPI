from fastapi import APIRouter

#
from src.application.responses import Respuesta
from src.application.use_cases.get_audio_iframe import UC_GetAudioIframe
from src.application.use_cases.download_audio import UC_AudioDownload
from src.presentation.dtos import DTO_GetAudioIframe, DTO_AudioDownload


router = APIRouter()


@router.post("/get_audio_iframe/")
async def get_audio_iframe(dto: DTO_GetAudioIframe) -> Respuesta:
    return await UC_GetAudioIframe(url=dto.url, platform=dto.platform).execute()


@router.post("/download_audio/")
async def download_audio(dto: DTO_AudioDownload):
    return await UC_AudioDownload(
        url=dto.url, title=dto.title, platform=dto.platform, quality=dto.quality
    ).execute()
