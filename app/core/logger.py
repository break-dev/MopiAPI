import logging
from logging.handlers import RotatingFileHandler
#
from core.settings import settings

# Logger
logger = logging.getLogger("mopi")
logger.setLevel(logging.INFO)

# Handlers: Stream + File
if not logger.handlers:
    # Formateador compartido
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    # Console (Stream)
    stream_h = logging.StreamHandler()
    stream_h.setFormatter(formatter)
    logger.addHandler(stream_h)

    # File con Rotación: 4MB por archivo, conserva el ultimo
    # 4MB = 4194304 bytes
    file_h = RotatingFileHandler(
        settings.LOG_FILE_PATH, maxBytes=4194304, backupCount=1
    )
    file_h.setFormatter(formatter)
    logger.addHandler(file_h)
