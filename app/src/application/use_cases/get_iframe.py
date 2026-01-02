import re
import requests
from typing import Literal
import httpx

#
from src.domain.enums import Platforms
from src.application.responses import (
    Respuesta,
    errorResponse,
    validResponse,
    RES_GetIframe,
)
from src.application.utils.utils import Utils
from core.logger import logger
from core.settings import settings


class UC_GetIframe:

    def __init__(
        self,
        url: str,
        platform: str,
    ):
        self.url = url
        self.platform = platform

    async def execute(self) -> Respuesta:
        try:
            # verificar dominio
            result = Utils().verify_domain(self.url, self.platform)
            if not result:
                return errorResponse("La url no es válida")

            if self.platform == Platforms.YOUTUBE.value:
                self.url = Utils().format_url_youtube(self.url)
            elif self.platform == Platforms.SOUNDCLOUD.value:
                self.url = Utils().format_url_soundcloud(self.url)

            # consultamos a la api de iframes
            async with httpx.AsyncClient() as client:
                result = await client.get(settings.API_IFRAME, params={"url": self.url})
            if result.status_code != 200:
                logger.error(f"Error al contactar con la API: {settings.API_IFRAME}")
                return errorResponse()

            # buscamos el url del iframe
            code = result.json().get("code", "")

            if not code:
                logger.error(
                    f"No se encontró el campo CODE para {self.platform}: {self.url}"
                )
                return errorResponse()

            if self.platform == Platforms.SOUNDCLOUD.value:
                pattern = r'src="(https://(?:w{1,3}\.)?soundcloud\.com/player/[^"]+)"'
            elif self.platform == Platforms.YOUTUBE.value:
                pattern = (
                    r'src="(https://(?:www\.)?youtube\.com/embed/[^"?]+(?:\?[^"]*)?)"'
                )

            match = re.search(pattern, code)

            if match:
                src_url = match.group(1)
                if self.platform == Platforms.SOUNDCLOUD.value:
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
