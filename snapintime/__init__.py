__author__ = "Eric Mesa"
__version__ = "1.3.1"
__license__ = "GNU GPL v3.0"
__copyright__: str = "(c) 2014 - 2022 Eric Mesa"
__email__: str = "ericsbinaryworld at gmail dot com"


import logging

from rich.logging import RichHandler

log = logging.getLogger("snapintime")
log.setLevel(logging.INFO)
RICH_FORMAT = logging.Formatter("%(message)s", "[%X]")
LOG_FILE_FORMAT = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler = logging.FileHandler('snap_in_time.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(LOG_FILE_FORMAT)
console_handler = RichHandler()
console_handler.setFormatter(RICH_FORMAT)
log.addHandler(file_handler)
log.addHandler(console_handler)
