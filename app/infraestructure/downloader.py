import yt_dlp
from pathlib import Path
from typing import Optional, Dict

from core.settings import settings
from shared.literals import DownloadMode
from shared.utils import Utils


class Downloader:
    def __init__(self, cookies_file: Optional[Path] = None):
        self.cookies_file = cookies_file or settings.COOKIES_FILE_PATH
        self.utils = Utils()

    def download(
        self,
        url: str,
        mode: DownloadMode,
        output_dir: Path,
    ) -> Path:
        try:
            ydl_opts = self._build_options(mode, output_dir)
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)

            file_path, file_name, ext, mime = self.utils.find_file_temp(output_dir)
            if not file_path:
                raise RuntimeError("No se encontró ningún archivo descargado")

            return file_path, file_name, ext, mime

        except Exception as e:
            raise e

    def _build_options(self, mode: DownloadMode, temp_dir: Path) -> Dict:
        opts = {
            "outtmpl": str(temp_dir / "%(title)s.%(ext)s"),
            "quiet": True,
            "no_warnings": True,
            "ignoreerrors": False,
            "extract_flat": False,
            "cookiefile": (
                str(self.cookies_file) if self.cookies_file.exists() else None
            ),
            "restrictfilenames": True,
            "windowsfilenames": True,
        }

        if mode == "audio":
            opts["format"] = "bestaudio/best[acodec!=none]"
            opts["format_sort"] = ["abr"]
            opts["postprocessors"] = [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "0",  # 0 = mejor calidad - 10 = peor calidad
                }
            ]
        else:  # video
            # Selector para mejor video y mejor audio, o fallback a mejor combinado
            opts["format"] = "bestvideo+bestaudio/best"
            # Ordenar por resolución (altura) descendente, y luego por codec y fps
            opts["format_sort"] = ["res", "vcodec", "fps"]
            opts["merge_output_format"] = "mp4"

        return opts
