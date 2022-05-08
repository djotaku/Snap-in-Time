__author__ = "Eric Mesa"
__version__ = "1.2.1"
__license__ = "GNU GPL v3.0"
__copyright__: str = "(c) 2014 - 2022 Eric Mesa"
__email__: str = "ericsbinaryworld at gmail dot com"


import logging
from rich.logging import RichHandler

FORMAT = "%(message)s"
logging.basicConfig(
    level="INFO", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)

log = logging.getLogger("rich")
