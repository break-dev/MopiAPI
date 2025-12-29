import os
from pathlib import Path
from pydantic_settings import BaseSettings
from dotenv import load_dotenv, find_dotenv

#

env_path = find_dotenv()
if env_path:
    load_dotenv(env_path)
else:
    raise Exception("No se encontró el archivo .env")

# ruta absoluta del directorio app
folder_app_path = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    APP_NAME: str = "MOPI"
    APP_DESCRIPTION: str = (
        "API de MOPI, desarrollada para descargar tu música favorita."
    )
    APP_VERSION: str = "1.0"
    APP_CLIENT: str = os.getenv("APP_CLIENT", "")
    API_IFRAME: str = os.getenv("API_IFRAME", "")
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "dev")
    COOKIES_FILE_PATH: str = f"{folder_app_path}/cookies.txt"
    DOWNLOAD_DIR_PATH: str = f"{folder_app_path}/downloads"
    LOG_FILE_PATH: str = f"{folder_app_path}/bitacora.log"

    def validate(self):
        """Verifica que las rutas y variables críticas estén configuradas correctamente."""
        if not self.API_IFRAME:
            raise Exception("API_IFRAME (variable de entorno vacía)")

        if not Path(self.COOKIES_FILE_PATH).is_file():
            Path(self.COOKIES_FILE_PATH).touch(exist_ok=True)
        if not Path(self.DOWNLOAD_DIR_PATH).is_dir():
            Path(self.DOWNLOAD_DIR_PATH).mkdir(exist_ok=True)
        if not Path(self.LOG_FILE_PATH).is_file():
            Path(self.LOG_FILE_PATH).touch(exist_ok=True)


# Instancia única y validación
settings = Settings()
settings.validate()
