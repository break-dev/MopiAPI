import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv, find_dotenv

#
from src.application.utils.utils import find_file_path, find_folder_path

env_path = find_dotenv()
if env_path:
    load_dotenv(env_path)


class Settings(BaseSettings):
    APP_NAME: str = "MOPI"
    APP_DESCRIPTION: str = (
        "API de MOPI, desarrollada para descargar tu música favorita."
    )
    APP_VERSION: str = "1.0"

    COOKIES_FILE_PATH: str = find_file_path("cookies.txt")
    DOWNLOAD_DIR_PATH: str = find_folder_path("downloads")
    API_IFRAME: str = os.getenv("API_IFRAME", "")

    def validate(self):
        """Verifica que las rutas y variables críticas estén configuradas correctamente."""
        missing = []
        if not self.COOKIES_FILE_PATH:
            missing.append("COOKIES_FILE_PATH (cookies.txt no encontrado)")
        if not self.DOWNLOAD_DIR_PATH:
            missing.append("DOWNLOAD_DIR_PATH (carpeta 'downloads' no encontrada)")
        if not self.API_IFRAME:
            missing.append("API_IFRAME (variable de entorno vacía)")

        if missing:
            raise Exception(
                "Error al preparar Settings:\n" + "\n".join(f"- {m}" for m in missing)
            )


# Instancia única y validación
settings = Settings()
settings.validate()
