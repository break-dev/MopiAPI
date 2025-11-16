import re
from typing import Optional
from enum import Enum
from abc import ABC, abstractmethod
from typing import Optional
from fastapi.responses import FileResponse

#
from src.domain.classes import AllPlatforms
from src.application.responses import validResponse, errorResponse, Respuesta
from src.application.responses import RES_FileResponse
from src.infraestructure.dlp import DLP
from src.application.utils.utils import (
    find_file_temp,
    verify_domain,
    format_url_youtube,
    create_temp_folder,
)


class UC_Download(ABC):

    def __init__(
        self,
        url: str,
        title: Optional[str],
        platform: Enum,
        duration_limits: dict,
        quality: Enum,
        codec: Enum,
    ):
        self.url = url
        self.title = title
        self.platform = platform
        self.duration_limits = duration_limits
        self.quality = quality
        self.codec = codec
        #
        self.folder_path: str = ""  # path de la carpeta que alojara el archivo
        self.file_path: str = ""  # path completo: folder + filename.ext
        self.file_name: str = ""  # nombre del archivo

    @abstractmethod
    def get_opts_for_download(self) -> dict:
        """Devuelve las opciones para descargar el audio."""
        pass

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
        # verificar el titulo, de ser necesario
        if self.title != None:
            result = self.verify_title()
            if not result:
                return "El título no es válido"

        # verificar si el dominio de la url coincide con la plataforma indicada
        result = verify_domain(self.url, self.platform.value)
        if not result:
            return "La url no es válida"

        if self.platform.value == AllPlatforms.YOUTUBE.value:
            result = format_url_youtube(self.url)
            if not result:
                return "La url no es válida"
            self.url = result

        # verificar si duracion es valida
        result = DLP().verify_duration(
            self.url, self.duration_limits, self.quality.value
        )
        if result:
            return result

        return ""

    async def execute(self) -> Respuesta:
        # verificar los datos de entrada
        result = self.verify_all()
        if result:
            return errorResponse(result)

        # descargamos
        self.folder_path = create_temp_folder()
        result = DLP().download(
            url=self.url,
            folder_path=self.folder_path,
            allowed_exts=[self.codec.value],
            opts_for_download=self.get_opts_for_download(),
        )
        if not result:
            return errorResponse()

        # obtenemos el path y el nombre del archivo de audio creado
        result = find_file_temp(
            self.folder_path,
            allowed_exts=[self.codec.value],  # filtra por mp3, mp4, etc.
        )

        self.file_path, self.file_name, extension = result  # type: ignore

        return validResponse(
            RES_FileResponse(
                title=self.title if self.title else self.file_name,
                extension=extension,
                file=FileResponse(self.file_path),
            )
        )
