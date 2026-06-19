from pydantic import BaseModel
from pathlib import Path

class RES_FileResponse(BaseModel):
    folder_name: str
    file_path: Path
    file_name: str
    extension: str
    media_type: str


class RES_GetIframe(BaseModel):
    url: str
