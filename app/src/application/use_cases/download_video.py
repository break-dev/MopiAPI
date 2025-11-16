import os
from typing import Optional

#
from core.settings import settings
from src.domain.classes import VideoCodecs, VideoQuality, VideoPlatforms
from src.application.use_cases.download import UC_Download


class UC_VideoDownload(UC_Download):

    def __init__(
        self,
        url: str,
        title: Optional[str],
        platform: VideoPlatforms,
        quality: VideoQuality,
    ):
        super().__init__(
            url=url,
            title=title,
            platform=platform,
            duration_limits={  # calidad
                "480": 16,
                "720": 12,
                "1080": 8,
                "1440": 4,
            },
            quality=quality,
            codec=VideoCodecs.MP4,
        )

    def get_opts_for_download(self) -> dict:
        outtmpl = os.path.join(self.folder_path, "%(title)s.%(ext)s")

        video_filter = f"bestvideo[height<={self.quality.value}]/bestvideo"
        audio_filter = "bestaudio/best"

        return {
            "format": f"{video_filter}+{audio_filter}",
            "merge_output_format": self.codec.value,
            "postprocessors": [
                {
                    "key": "FFmpegVideoConvertor",
                    "preferredformat": self.codec.value,
                }
            ],
            "outtmpl": outtmpl,
            "noplaylist": True,
            "quiet": True,
            "no_warnings": False,
            "ignoreerrors": True,
            "writethumbnail": False,
            "writeinfojson": False,
            "cookiefile": settings.COOKIES_FILE_PATH,
        }
