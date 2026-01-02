from typing import List

#
from src.domain.enums import Platforms

domains_youtube = [
    "youtube.com",
    "www.youtube.com",
    "m.youtube.com",
    "youtu.be",
    "youtube-nocookie.com",
    "music.youtube.com",
    "gaming.youtube.com",
    "kids.youtube.com",
    "ytimg.com",
    "yt.be",
]

domains_soundcloud = [
    "soundcloud.com",
    "www.soundcloud.com",
    "m.soundcloud.com",
    "snd.sc",
]


def get_domains(platform: str) -> List[str]:
    if platform == Platforms.YOUTUBE.value:
        return domains_youtube
    elif platform == Platforms.SOUNDCLOUD.value:
        return domains_soundcloud
    else:
        return []
