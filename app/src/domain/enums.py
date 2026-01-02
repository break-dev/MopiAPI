from enum import Enum


class AudioQuality(Enum):
    LOW = "128"
    MEDIUM = "192"
    HIGH = "256"
    VERY_HIGH = "320"


class VideoQuality(Enum):
    LOW = "480"
    MEDIUM = "720"
    HIGH = "1080"
    VERY_HIGH = "1440"


class VideoCodecs(Enum):
    MP4 = "mp4"
    MKV = "mkv"
    AVI = "avi"


class AudioCodecs(Enum):
    MP3 = "mp3"
    WAV = "wav"
    FLAC = "flac"


class Mode(Enum):
    AUDIO = "audio"
    VIDEO = "video"


class Platforms(Enum):
    YOUTUBE = "youtube"
    SOUNDCLOUD = "soundcloud"
