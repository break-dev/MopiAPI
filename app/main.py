from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from slowapi import Limiter
from slowapi.util import get_remote_address
from fastapi import BackgroundTasks
from fastapi.responses import FileResponse
import mimetypes

mimetypes.init()


#
from core.settings import settings
from src.presentation.filter_exception import filter_exception
from src.application.responses import Respuesta, RES_FileResponse
from src.application.utils.utils import Utils
from src.application.use_cases.get_iframe import UC_GetIframe
from src.application.use_cases.download import UC_Download
from src.presentation.dtos import (
    DTO_GetAudioIframe,
    DTO_GetVideoIframe,
    DTO_AudioDownload,
    DTO_VideoDownload,
)


# fastapi dev app/main.py
#
# cd app
# fastapi dev main.py

app = FastAPI(
    title=settings.APP_NAME,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION,
)

# rate limit
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter


# Registrar el filtro global de excepciones
filter_exception(app)


# Middleware para corregir esquema HTTPS si viene tras proxy
@app.middleware("http")
async def https_scheme(request: Request, call_next):
    proto = request.headers.get("X-Forwarded-Proto", "").lower()
    if proto == "https":
        request.scope["scheme"] = "https"
    return await call_next(request)


# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*" if not settings.APP_CLIENT else settings.APP_CLIENT],
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["*"],
)

# ------- ENDPOINTS ------------


@app.post("/get_audio_iframe/")
@limiter.limit("10/minute")
async def get_audio_iframe(dto: DTO_GetAudioIframe, request: Request) -> Respuesta:
    uc = UC_GetIframe(url=dto.url, platform=dto.platform.value, file_type="video")
    return await uc.execute()


@app.post("/get_video_iframe/")
@limiter.limit("10/minute")
async def get_video_iframe(dto: DTO_GetVideoIframe, request: Request) -> Respuesta:
    uc = UC_GetIframe(url=dto.url, platform=dto.platform.value, file_type="video")
    return await uc.execute()


@app.post("/download_audio/")
@limiter.limit("4/minute")
async def download_audio(dto: DTO_AudioDownload, request: Request):
    uc = UC_Download(
        url=dto.url,
        title=dto.title,
        platform=dto.platform.value,
        quality=dto.quality.value,
        file_type="audio",
    )
    result = await uc.execute()

    if not result.success or not result.data:
        return result

    data: RES_FileResponse = result.data  # type: ignore

    # programar eliminacion de la carpeta
    background_tasks = BackgroundTasks()
    background_tasks.add_task(Utils().delete_temp_folder, data.folder_name)

    return FileResponse(
        path=data.file_path,
        filename=f"{data.file_name}.{data.extension}",
        media_type="audio/mpeg",
        background=background_tasks,
    )


@app.post("/download_video/")
@limiter.limit("4/minute")
async def download_video(dto: DTO_VideoDownload, request: Request):
    uc = UC_Download(
        url=dto.url,
        title=dto.title,
        platform=dto.platform.value,
        quality=dto.quality.value,
        file_type="video",
    )
    result = await uc.execute()

    if not result.success or not result.data:
        return result

    data: RES_FileResponse = result.data  # type: ignore

    # programar eliminacion de la carpeta
    background_tasks = BackgroundTasks()
    background_tasks.add_task(Utils().delete_temp_folder, data.folder_name)

    return FileResponse(
        path=data.file_path,
        filename=f"{data.file_name}.{data.extension}",
        media_type=data.media_type,
        background=background_tasks,
    )


# run run
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
