import re
from typing import Optional
from pathlib import Path

#
from core.settings import settings
from use_cases._responses import RES_FileResponse
from shared._response import ApiResponse, error_response, valid_response
from infraestructure.downloader import Downloader
from shared.utils import Utils
from shared.literals import DownloadMode, Platforms


class UC_Download:

    def __init__(
        self,
        url: str,
        title: Optional[str],
        platform: Platforms,
        mode: DownloadMode,
    ):
        self.url: str = url
        self.title: Optional[str] = title
        self.platform: Platforms = platform
        self.mode: DownloadMode = mode

        #
        self.folder_path: Path = Path("")  # path de la carpeta que alojara el archivo
        self.file_path: Path = Path("")  # path del archivo (folder + filename.ext)
        self.file_name: str = ""  # nombre del archivo (filename)
        self.extension: str = ""  # extension del archivo (ext)
        self.media_type: str = ""  # tipo de archivo (mimetype)

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
        # verificar el titulo, si es proporcionado
        if self.title != None:
            is_valid = self.verify_title()
            if not is_valid:
                return "El título no es válido"

        # verificar si el dominio de la url coincide con la plataforma indicada
        is_valid = Utils().verify_domain(self.url, self.platform)
        if not is_valid:
            return "La url no es válida"

        # formateamos las urls segun la plataforma
        if self.platform == "youtube":
            url_format = Utils().format_url_youtube(self.url)
        elif self.platform == "soundcloud":
            url_format = Utils().format_url_soundcloud(self.url)

        if not url_format:
            return "La url no es válida"
        self.url = url_format

        return ""

    def download(self) -> bool:
        self.folder_path = Utils().create_temp_folder()

        (
            self.file_path,
            self.file_name,
            self.extension,
            self.media_type,
        ) = Downloader().download(
            url=self.url,
            mode=self.mode,
            output_dir=self.folder_path,
        )

        if not self.file_path:
            # Limpiar carpeta temporal en caso de error
            Utils().delete_temp_folder(self.folder_path)
            return False
        return True

    async def execute(self) -> ApiResponse:
        # verificar los datos de entrada
        error = self.verify_all()
        if error:
            return error_response(error)

        # descargamos
        if not self.download():
            return error_response()

        return valid_response(
            RES_FileResponse(
                folder_name=self.folder_path.name,
                file_name=self.title if self.title else self.file_name,
                file_path=self.file_path,
                extension=self.extension,
                media_type=self.media_type,
            )
        )
