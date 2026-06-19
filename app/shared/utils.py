from typing import Tuple, List
from pathlib import Path
import mimetypes
import re
import shutil
import uuid
from urllib.parse import urlparse, parse_qs

#
from core.settings import settings
from shared.variables import domains_youtube, domains_soundcloud
from shared.literals import Platforms


class Utils:

    # Obtener dominios según la plataforma
    def get_domains(self, platform: Platforms) -> List[str]:
        match platform:
            case "youtube":
                return domains_youtube
            case "soundcloud":
                return domains_soundcloud
            case _:
                return []

    # Verifirar dominio segun la plataforma
    def verify_domain(self, url: str, platform: Platforms) -> bool:
        try:
            parsed = urlparse(url)
            netloc = parsed.netloc.lower()
            return any(
                netloc.endswith(domain.lower()) for domain in self.get_domains(platform)
            )
        except Exception:
            return False

    # Normaliza una URL de YouTube
    def format_url_youtube(self, url: str) -> str:
        parsed = urlparse(url.strip())
        netloc = parsed.netloc.lower()

        video_id = None

        # youtube.com/watch?v=VIDEO_ID
        if "youtube.com" in netloc:
            query = parse_qs(parsed.query)
            v = query.get("v")
            if v and re.fullmatch(r"[\w-]{11}", v[0]):
                video_id = v[0]

        # youtu.be/VIDEO_ID
        elif "youtu.be" in netloc:
            match = re.fullmatch(r"/([\w-]{11})", parsed.path)
            if match:
                video_id = match.group(1)

        # Si se encontró video_id, retornamos la URL normalizada
        if video_id:
            return f"https://www.youtube.com/watch?v={video_id}"
        else:
            return ""

    # Normaliza una URL de Soundcloud
    def format_url_soundcloud(self, url: str) -> str:
        parsed = urlparse(url.strip())
        netloc = parsed.netloc.lower()

        if "soundcloud.com" not in netloc:
            return ""

        # /artist/track
        path_parts = parsed.path.strip("/").split("/")

        # verificamos que tenga el usuario y el track
        if len(path_parts) >= 2:
            clean_path = f"/{path_parts[0]}/{path_parts[1]}"
            return f"https://soundcloud.com{clean_path}"

        return ""

    # Busca un archivo dentro del directorio
    # Devuelve: (file_path, file_name, extension, media_type)
    def find_file_temp(self, folder_path: Path) -> Tuple[Path, str, str, str]:
        file_path: Path = Path("")
        extension = ""
        file_name = ""
        media_type = ""
        try:
            if not folder_path.exists() or not folder_path.is_dir():
                raise

            for item in folder_path.iterdir():
                if item.is_file():
                    ext = item.suffix.lower().replace(".", "")

                    file_path = item.resolve()
                    file_name = item.stem
                    extension = ext
                    media_type, _ = mimetypes.guess_type(file_path)
                    break

        finally:
            return file_path, file_name, extension, media_type if media_type else ""

    # Crea una carpeta dentro de DOWNLOAD_DIR_PATH.
    # Devuelve la ruta absoluta como Path.
    def create_temp_folder(self) -> Path:
        target_path = settings.DOWNLOAD_DIR_PATH / str(uuid.uuid4())
        target_path.mkdir(parents=True, exist_ok=True)
        return target_path.resolve()

    # Elimina una carpeta dentro de DOWNLOAD_DIR_PATH y devuelve True si se eliminó
    # correctamente, False en caso de error o si no existe.
    def delete_temp_folder(self, folder_path: Path) -> bool:
        if not folder_path.exists() or not folder_path.is_dir():
            return False

        try:
            shutil.rmtree(folder_path)
            return True
        except Exception:
            return False
