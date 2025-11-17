import logging

#
from src.application.utils.utils import Utils

# Logger
logger = logging.getLogger("mopi")
logger.setLevel(logging.INFO)

# Handlers: Stream + File
if not logger.handlers:

    stream_h = logging.StreamHandler()
    stream_h.setFormatter(
        logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    )
    logger.addHandler(stream_h)

    # File handler opcional
    file_h = logging.FileHandler(Utils().find_file_path("bitacora.log"))
    file_h.setFormatter(
        logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    )
    logger.addHandler(file_h)
