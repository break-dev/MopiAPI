import os
from pathlib import Path
from pydantic_settings import BaseSettings
from dotenv import load_dotenv, find_dotenv

# Cargar .env
env_path = find_dotenv()
if not env_path:
    raise Exception("No se encontró el archivo .env")
load_dotenv(env_path)

# Ruta base
BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    # Pydantic ya tiene los valores de .env
    APP_NAME: str = "MOPI"
    APP_DESCRIPTION: str = (
        "API de MOPI, desarrollada para descargar tu música favorita."
    )
    APP_VERSION: str = "1.0"
    APP_CLIENT: str = ""
    API_IFRAME: str = ""
    ENVIRONMENT: str = "dev"

    # Rutas
    COOKIES_FILE_PATH: Path = BASE_DIR / "cookies.txt"
    DOWNLOAD_DIR_PATH: Path = BASE_DIR / "downloads"
    LOG_FILE_PATH: Path = BASE_DIR / "bitacora.log"

    def validate(self):
        """Verifica y crea archivos/carpetas."""
        if not self.API_IFRAME:
            raise ValueError("Falta API_IFRAME en el .env")

        self.COOKIES_FILE_PATH.touch(exist_ok=True)
        self.DOWNLOAD_DIR_PATH.mkdir(exist_ok=True, parents=True)
        self.LOG_FILE_PATH.touch(exist_ok=True)


# Instancia
settings = Settings()
settings.validate()
