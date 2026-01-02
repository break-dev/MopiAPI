import yt_dlp
from pathlib import Path
from typing import List, Tuple, Literal
import os

#
from core.logger import logger
from core.settings import settings
from src.application.utils.utils import Utils
from src.domain.enums import AudioCodecs


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

    def get_opts_for_download_audio(
        self, folder_path: str, codec: str, quality: str
    ) -> dict:
        outtmpl = os.path.join(folder_path, "%(title)s.%(ext)s")

        if codec == AudioCodecs.MP3.value:
            postprocessors = [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": codec,
                    "preferredquality": quality,
                },
                {"key": "FFmpegMetadata"},
            ]
        else:
            postprocessors = [
                {"key": "FFmpegExtractAudio", "preferredcodec": codec},
                {"key": "FFmpegMetadata"},
            ]

        return {
            # --- FORMATO ---
            "format": "bestaudio/best",
            "prefer_free_formats": True,
            "allow_unplayable_formats": False,
            # --- OUTPUT ---
            "outtmpl": outtmpl,
            "restrictfilenames": False,
            "windowsfilenames": True,
            "trim_file_name": 200,
            # --- POSTPROCESSORS ---
            "postprocessors": postprocessors,
            # --- PLAYLIST CONTROL ---
            "noplaylist": True,
            "ignoreerrors": True,
            "skip_playlist_after_errors": 0,
            # --- RED / SSL / USER-AGENT ---
            "http_headers": {
                "User-Agent": "Mozilla/5.0",
                "Accept-Language": "en-US,en;q=0.9",
            },
            "nocheckcertificate": False,
            "socket_timeout": 30,
            # --- RETRIES ROBUSTOS ---
            "retries": 10,
            "file_access_retries": 10,
            "fragment_retries": 15,
            "extractor_retries": 5,
            # --- FRAGMENTOS / STREAMING ---
            "skip_unavailable_fragments": True,
            "continuedl": True,
            "nopart": False,
            "hls_use_mpegts": True,
            "dynamic_mpd": True,
            # --- RUIDO ---
            "quiet": True,
            "no_warnings": True,
            # --- FIXES ---
            "fixup": "detect_or_warn",  # conserva tu lógica
            #
            # Cookies: obligatorio para videos con restricciones regionales
            #
            "cookiefile": settings.COOKIES_FILE_PATH,
            "paths": {
                "home": settings.DOWNLOAD_DIR_PATH,
                "temp": settings.DOWNLOAD_DIR_PATH,
            },
            "cachedir": settings.DOWNLOAD_DIR_PATH,
        }

    def get_opts_for_download_video(self, folder_path: str, codec: str) -> dict:
        outtmpl = os.path.join(folder_path, "%(title)s.%(ext)s")

        return {
            "merge_output_format": codec,
            "outtmpl": outtmpl,
            # Mejora la estabilidad al seleccionar streams correctos
            "ignore_no_formats_error": True,
            "allow_unplayable_formats": False,
            "force_overwrites": True,
            "noplaylist": True,
            "quiet": True,
            "no_warnings": False,
            "ignoreerrors": True,
            # Headers realistas que evitan rate limiting
            "http_headers": {
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/124.0 Safari/537.36"
                ),
                "Accept-Language": "en-US,en;q=0.9",
                "Referer": "https://www.youtube.com/",
            },
            # Cookies
            "cookiefile": settings.COOKIES_FILE_PATH,
            # Limitar interacciones externas
            "socket_timeout": 20,
            "retries": 3,
            "fragment_retries": 10,
            "paths": {
                "home": settings.DOWNLOAD_DIR_PATH,
                "temp": settings.DOWNLOAD_DIR_PATH,
            },
            "cachedir": settings.DOWNLOAD_DIR_PATH,
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
        file_type: Literal["audio", "video"],
        codec: str,
        quality: str,
    ) -> Tuple[str, str, str, str]:
        """(file_path, file_name, extension, media_type)"""
        file_path = ""
        file_name = ""
        extension = ""
        media_type = ""
        try:
            if file_type == "audio":
                with yt_dlp.YoutubeDL(self.get_opts_for_download_audio(folder_path=folder_path, codec=codec, quality=quality)) as ydl:  # type: ignore
                    ydl.download(url)
            elif file_type == "video":
                with yt_dlp.YoutubeDL(self.get_opts_for_download_video(folder_path=folder_path, codec=codec)) as ydl:  # type: ignore
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
