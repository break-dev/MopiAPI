import re
import httpx

#
from shared.literals import Platforms
from use_cases._responses import RES_GetIframe
from shared.utils import Utils
from core.logger import logger
from core.settings import settings
from shared._response import ApiResponse, error_response, valid_response


class UC_GetIframe:

    def __init__(
        self,
        url: str,
        platform: Platforms,
    ):
        self.url: str = url
        self.platform: Platforms = platform

    async def execute(self) -> ApiResponse:
        try:
            # verificar dominio
            result = Utils().verify_domain(self.url, self.platform)
            if not result:
                return error_response("La url no es válida")

            if self.platform == "youtube":
                self.url = Utils().format_url_youtube(self.url)
            elif self.platform == "soundcloud":
                self.url = Utils().format_url_soundcloud(self.url)

            # consultamos a la api de iframes
            async with httpx.AsyncClient() as client:
                result = await client.get(settings.API_IFRAME, params={"url": self.url})
            if result.status_code != 200:
                logger.error(f"Error al contactar con la API: {settings.API_IFRAME}")
                return error_response()

            # buscamos el url del iframe
            code = result.json().get("code", "")

            if not code:
                logger.error(
                    f"No se encontró el campo CODE para {self.platform}: {self.url}"
                )
                return error_response()

            if self.platform == "soundcloud":
                pattern = r'src="(https://(?:w{1,3}\.)?soundcloud\.com/player/[^"]+)"'
            elif self.platform == "youtube":
                pattern = (
                    r'src="(https://(?:www\.)?youtube\.com/embed/[^"?]+(?:\?[^"]*)?)"'
                )

            match = re.search(pattern, code)

            if match:
                src_url = match.group(1)
                if self.platform == "soundcloud":
                    src_url += "&show_comments=false"

                return valid_response(RES_GetIframe(url=src_url))
            else:
                logger.warning(
                    f"No se encontró iframe para {self.platform}: {self.url}"
                )
                return error_response()

        except Exception as e:
            logger.error(f"Error en UC_GetIframe ({self.platform}): {e}")
            return error_response()
