from typing import Tuple, Optional, List
from pathlib import Path
import re
import shutil
import uuid
from urllib.parse import urlparse, parse_qs

#
from core.logger import logger
from src.application.utils.domains import get_domains


def verify_domain(url: str, platform: str) -> bool:
    """Verifica si el dominio del URL coincide con alguno en la lista."""
    try:
        parsed = urlparse(url)
        netloc = parsed.netloc.lower()
        return any(netloc.endswith(domain.lower()) for domain in get_domains(platform))
    except Exception:
        return False


def format_url_youtube(url: str) -> str:
    """Normaliza una URL de YouTube"""
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


def find_file_temp(
    folder_path: str, allowed_exts: List[str]
) -> Optional[Tuple[str, str, str]]:
    """
    Busca un archivo dentro del directorio y filtra por extensiones permitidas.
    Devuelve:
        (file_path, filename_sin_extension, extension)
    """
    try:
        folder = Path(folder_path)
        if not folder.exists() or not folder.is_dir():
            return None

        for item in folder.iterdir():
            if item.is_file():
                ext = item.suffix.lower().replace(".", "")

                if ext not in allowed_exts:
                    continue  # descartar archivos basura

                return (
                    str(item.resolve()),
                    item.stem,  # nombre sin extensión
                    ext,  # extensión detectada
                )

        return None

    except Exception as e:
        logger.exception(f"Error en find_file_temp: {e}")
        return None


def find_file_path(file_name: str) -> str:
    """Busca un archivo en el directorio actual y sus padres."""
    current_path = Path(__file__).resolve().parent
    for directory in [current_path] + list(current_path.parents):
        file_path = directory / file_name
        if file_path.is_file():
            return str(file_path.resolve())

    return ""


def find_folder_path(folder_name: str) -> str:
    """Busca una carpeta en el directorio actual y sus padres."""
    current_path = Path(__file__).resolve().parent
    for directory in [current_path] + list(current_path.parents):
        folder_path = directory / folder_name
        if folder_path.is_dir():
            return str(folder_path.resolve())
    return ""


def create_temp_folder() -> str:
    """
    Crea una carpeta dentro de DOWNLOAD_DIR_PATH.
    Devuelve la ruta absoluta como string.
    """
    from core.settings import settings

    folder_name = str(uuid.uuid4())
    folder_path = settings.DOWNLOAD_DIR_PATH

    base_path = Path(folder_path)
    target_path = base_path / folder_name

    target_path.mkdir(parents=True, exist_ok=True)
    return str(target_path.resolve())


def delete_temp_folder(folder_name: str) -> bool:
    """
    Elimina una carpeta dentro de DOWNLOAD_DIR_PATH junto con todo su contenido.
    Devuelve True si se eliminó correctamente, False en caso de error o si no existe.
    """
    from core.settings import settings

    base_path = Path(settings.DOWNLOAD_DIR_PATH)
    target_path = base_path / folder_name

    if not target_path.exists() or not target_path.is_dir():
        return False

    try:
        shutil.rmtree(target_path)
        return True
    except Exception:
        return False
