import re
import requests

#
from src.domain.classes import AllPlatforms
from src.application.responses import (
    Respuesta,
    errorResponse,
    validResponse,
    RES_GetIframe,
)
from src.application.utils.utils import utils
from core.logger import logger
from core.settings import settings


class UC_GetAudioIframe:

    def __init__(self, url: str, platform: str):
        self.url = url
        self.platform = platform

    async def execute(self) -> Respuesta:
        try:
            result = utils.verify_domain(self.url, self.platform)
            if not result:
                return errorResponse("La url no es válida")

            if self.platform == AllPlatforms.YOUTUBE.value:
                self.url = utils.format_url_youtube(self.url)

            result = requests.get(settings.API_IFRAME, params={"url": self.url})

            if result.status_code != 200:
                logger.error(f"Error al contactar con la API: {settings.API_IFRAME}")
                return errorResponse()

            code = result.json().get("code", "")

            # Escoger patrón según plataforma
            if self.platform == AllPlatforms.SOUNDCLOUD.value:
                pattern = r'src="(https://(?:w{1,3}\.)?soundcloud\.com/player/[^"]+)"'
            elif self.platform == AllPlatforms.YOUTUBE.value:
                pattern = (
                    r'src="(https://(?:www\.)?youtube\.com/embed/[^"?]+(?:\?[^"]*)?)"'
                )

            match = re.search(pattern, code)

            if match:
                src_url = match.group(1)
                if self.platform == AllPlatforms.SOUNDCLOUD.value:
                    src_url += "&show_comments=false"

                return validResponse(RES_GetIframe(url=src_url))
            else:
                logger.warning(
                    f"No se encontró iframe para {self.platform}: {self.url}"
                )
                return errorResponse()

        except Exception as e:
            logger.error(f"Error en UC_GetIframe ({self.platform}): {e}")
            return errorResponse()
