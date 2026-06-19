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
from presentation.filter_exception import filter_exception
from shared.utils import Utils
from use_cases._responses import RES_FileResponse, RES_GetIframe
from use_cases.get_iframe import UC_GetIframe
from use_cases.download import UC_Download
from presentation.dtos import DTO_GetIframe, DTO_Download
from shared.literals import DownloadMode
from shared._response import ApiResponse

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
    expose_headers=["Content-Disposition"],
)

# ------- ENDPOINTS ------------


@app.post("/get_iframe/")
@limiter.limit("20/minute")
async def get_iframe(dto: DTO_GetIframe, request: Request) -> ApiResponse:
    uc = UC_GetIframe(url=dto.url, platform=dto.platform)
    return await uc.execute()


@app.post("/download/")
@limiter.limit("6/minute")
async def download(dto: DTO_Download, request: Request):
    uc = UC_Download(
        url=dto.url,
        title=dto.title,
        platform=dto.platform,
        mode=dto.mode,
    )
    result: ApiResponse = await uc.execute()

    if not result.success or not result.data:
        return result

    data: RES_FileResponse = result.data  # type: ignore

    # programar eliminacion de la carpeta
    background_tasks = BackgroundTasks()
    background_tasks.add_task(Utils().delete_temp_folder, data.file_path.parent)

    return FileResponse(
        path=data.file_path,
        filename=f"{data.file_name}.{data.extension}",
        media_type=data.media_type,
        background=background_tasks,
    )


# run run
if __name__ == "__main__":
    uvicorn.run(app, port=8080)
