import re
from typing import Optional, Literal
from pathlib import Path

#
from core.settings import settings
from src.application.responses import (
    validResponse,
    errorResponse,
    Respuesta,
    RES_FileResponse,
)
from src.infraestructure.dlp import DLP
from src.application.utils.utils import Utils
from src.domain.enums import AudioCodecs, AudioQuality, Mode, Platforms, VideoCodecs


class UC_Download:

    def __init__(
        self,
        url: str,
        title: Optional[str],
        platform: str,
        quality: str,
        mode: str,
    ):
        self.url = url
        self.title = title
        self.platform = platform
        self.quality = quality
        self.mode: str = mode
        #
        self.codec = (
            VideoCodecs.MP4.value if mode == Mode.VIDEO.value else AudioCodecs.MP3.value
        )
        self.duration_limits = (
            {  # calidad de video
                "480": 16,
                "720": 12,
                "1080": 8,
                "1440": 4,
            }
            if mode == Mode.VIDEO.value
            else {  # kbps
                "128": 16,
                "192": 12,
                "256": 8,
                "320": 4,
            }
        )
        #
        self.folder_path: str = ""  # path de la carpeta que alojara el archivo
        self.file_path: str = ""  # path del archivo (folder + filename.ext)
        self.file_name: str = ""  # nombre del archivo (filename)
        self.extension: str = ""  # extension del archivo (ext)
        self.media_type: str = ""  # tipo de archivo (mimetype)
        self.dlp = DLP()  # instancia de DLP

    def verify_title(self) -> bool:
        """Valida que el título sea aceptable (sin caracteres prohibidos y con longitud <= 64)."""
        if not self.title:
            return False

        invalid_chars = r'[<>:"/\\|?*\n\r\t]'
        title = self.title.strip()
        if re.search(invalid_chars, title) or len(title) > 64:
            return False
        return True

    def verify_all(self) -> str:
        result = False
        # verificar el titulo, si es proporcionado
        if self.title != None:
            result = self.verify_title()
            if not result:
                return "El título no es válido"

        # verificar si el dominio de la url coincide con la plataforma indicada
        result = Utils().verify_domain(self.url, self.platform)
        if not result:
            return "La url no es válida"

        if self.platform == Platforms.YOUTUBE.value:
            result = Utils().format_url_youtube(self.url)
            if not result:
                return "La url no es válida"
            self.url = result
        elif self.platform == Platforms.SOUNDCLOUD.value:
            result = Utils().format_url_soundcloud(self.url)
            if not result:
                return "La url no es válida"
            self.url = result

        # si se ejecuta en desarrollo, no verificamos la duracion
        if settings.ENVIRONMENT == "dev":
            return ""

        # verificar si la duracion es valida
        result = self.dlp.verify_duration(self.url, self.duration_limits, self.quality)
        if result:
            return result

        return ""

    def download(self) -> bool:
        self.folder_path = Utils().create_temp_folder()

        (
            self.file_path,
            self.file_name,
            self.extension,
            self.media_type,
        ) = self.dlp.download(
            url=self.url,
            folder_path=self.folder_path,
            mode=self.mode,
            codec=self.codec,
            quality=self.quality,
        )

        if not self.file_path:
            return False
        return True

    async def execute(self) -> Respuesta:
        # verificar los datos de entrada
        result = self.verify_all()
        if result:
            return errorResponse(result)

        # descargamos
        if not self.download():
            return errorResponse()

        return validResponse(
            RES_FileResponse(
                folder_name=Path(self.folder_path).name,
                file_name=self.title if self.title else self.file_name,
                file_path=self.file_path,
                extension=self.extension,
                media_type=self.media_type,
            )
        )
