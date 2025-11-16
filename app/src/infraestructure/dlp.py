import yt_dlp
from pathlib import Path
from typing import List

#
from core.logger import logger
from core.settings import settings
from src.application.utils.utils import (
    delete_temp_folder,
    find_file_temp,
)


class DLP:

    def get_opts_for_info(self) -> dict:
        """Devuelve las opciones para extraer información."""
        return {
            "quiet": True,
            "no_warnings": True,
            "simulate": True,  # simular descarga
            "ie_key": "Generic",
            "cookiefile": settings.COOKIES_FILE_PATH,
        }

    def verify_duration(self, url: str, duration_limits: dict, quality: str) -> str:
        """
        Verifica la duración del contenido
        """
        max_duration = duration_limits.get(quality)

        try:
            with yt_dlp.YoutubeDL(self.get_opts_for_info()) as ydl:  # type: ignore
                info = ydl.extract_info(url=url, download=False, ie_key="Generic")

            if info is None:
                return "No se pudo obtener información"

            duration = info.get("duration")  # en segundos

            if not duration or duration is None:
                return "No se pudo obtener información"

            if max_duration is not None and duration / 60 > max_duration:
                return f"La duración excede el límite de {max_duration} minutos"
            else:
                return ""

        except Exception as e:
            logger.exception(f"Error en verify_duration: {e}")
            return "No se pudo obtener información"

    def download(
        self,
        url: str,
        folder_path: str,
        allowed_exts: List[str],
        opts_for_download: dict,
    ) -> bool:
        try:
            with yt_dlp.YoutubeDL(opts_for_download) as ydl:  # type: ignore
                ydl.download(url)

            # verificar si se creo el archivo
            result = find_file_temp(folder_path, allowed_exts)
            if not result:
                logger.error("Archivo no encontrado después de la descarga.")
                delete_temp_folder(Path(folder_path).name)
                return False
            return True

        except Exception as e:
            logger.exception(f"Error en download: {e}")
            return False
