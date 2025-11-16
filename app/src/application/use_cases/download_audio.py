import os
from typing import Optional

#
from core.settings import settings
from src.domain.classes import AudioCodecs, AudioQuality, AudioPlatforms
from src.application.use_cases.download import UC_Download


class UC_AudioDownload(UC_Download):
    def __init__(
        self,
        url: str,
        title: Optional[str],
        platform: AudioPlatforms,
        quality: AudioQuality,
    ):
        super().__init__(
            url=url,
            title=title,
            platform=platform,
            duration_limits={  # kbps
                "128": 16,
                "192": 12,
                "256": 8,
                "320": 4,
            },
            quality=quality,
            codec=AudioCodecs.MP3,
        )

    def get_opts_for_download(self) -> dict:
        outtmpl = os.path.join(self.folder_path, "%(title)s.%(ext)s")
        postprocessors = ""

        if self.codec.value == AudioCodecs.MP3.value:
            postprocessors = [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": self.codec.value,
                    "preferredquality": self.quality.value,
                }
            ]
        # si son formatos lossless
        else:
            postprocessors = [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": self.codec.value,
                }
            ]

        return {
            "format": "bestaudio/best",
            "postprocessors": postprocessors,
            "outtmpl": outtmpl,
            "noplaylist": True,
            "quiet": True,
            "no_warnings": False,
            "ignoreerrors": True,
            "writethumbnail": False,
            "writeinfojson": False,
            "cookiefile": settings.COOKIES_FILE_PATH,
        }
