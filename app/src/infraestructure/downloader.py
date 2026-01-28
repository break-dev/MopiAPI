from yt_dlp import YoutubeDL
from pathlib import Path
from typing import Tuple, Literal
import os

#
from core.logger import logger
from core.settings import settings
from src.application.utils.utils import Utils


class Downloader:

    def _get_common_opts(self) -> dict:
        """Opciones compartidas para evitar duplicación y errores de JS/403."""
        return {
            "javascript_runtimes": ["node", "quickjs", "deno"],
            #
            # Extrae cookies del navegador principal
            # "cookiesfrombrowser": ("chrome",),
            #
            # Extrae cookies manualmente
            # "cookiefile": settings.COOKIES_FILE_PATH,
            #
            # Compatibilidad con SABR y nuevos protocolos
            "extractor_args": {
                "youtube": {
                    "player_client": ["android", "web"],
                    "skip": ["dash", "hls"],
                }
            },
            "quiet": True,
            "no_warnings": False,  # Útil dejarlo en False para debuggear cambios de YT
            # YouTube requiere su extractor específico ahora
            "force_generic_extractor": False,
            # "ie_key": "Generic",
        }

    def get_opts_for_info(self) -> dict:
        opts = self._get_common_opts()
        opts.update(
            {
                "simulate": True,
            }
        )
        return opts

    def get_opts_for_download_audio(
        self, folder_path: str, codec: str, quality: str
    ) -> dict:
        outtmpl = os.path.join(folder_path, "%(title)s.%(ext)s")
        opts = self._get_common_opts()
        opts.update(
            {
                "format": "bestaudio/best",
                "postprocessors": [
                    {
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": codec,
                        "preferredquality": quality,
                    }
                ],
                "outtmpl": outtmpl,
                "noplaylist": True,
                "ignoreerrors": True,
            }
        )
        return opts

    def get_opts_for_download_video(self, folder_path: str, codec: str) -> dict:
        outtmpl = os.path.join(folder_path, "%(title)s.%(ext)s")
        opts = self._get_common_opts()
        opts.update(
            {
                "format": "bestvideo+bestaudio/best",
                "merge_output_format": codec,
                "outtmpl": outtmpl,
                "noplaylist": True,
                "ignoreerrors": True,
            }
        )
        return opts

    def verify_duration(self, url: str, duration_limits: dict, quality: str) -> str:
        """
        Verifica la duración del contenido
        """
        max_duration = duration_limits.get(quality)

        try:
            with YoutubeDL(self.get_opts_for_info()) as ydl:
                info = ydl.extract_info(url=url, download=False)

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
        mode: Literal["audio", "video"],
        codec: str,
        quality: str,
    ) -> Tuple[str, str, str, str]:
        """(file_path, file_name, extension, media_type)"""
        file_path = ""
        file_name = ""
        extension = ""
        media_type = ""
        try:
            if mode == "audio":
                with YoutubeDL(
                    self.get_opts_for_download_audio(
                        folder_path=folder_path, codec=codec, quality=quality
                    )
                ) as ydl:
                    ydl.download(url)
            elif mode == "video":
                with YoutubeDL(
                    self.get_opts_for_download_video(
                        folder_path=folder_path, codec=codec
                    )
                ) as ydl:
                    ydl.download(url)
            else:
                raise Exception("Tipo de archivo no válido")

            # verificar si se creo el archivo
            result = Utils().find_file_temp(folder_path)
            if not result[0] or not result[1] or not result[2] or not result[3]:
                Utils().delete_temp_folder(Path(folder_path).name)
                raise Exception("Archivo no encontrado después de la descarga.")

            file_path, file_name, extension, media_type = result

        except Exception as e:
            logger.exception(f"Error en download: {e}")
        finally:
            return file_path, file_name, extension, media_type
