__author__ = "Eric Mesa"
__version__ = "3.1.2"
__license__ = "GNU GPL v3.1"
__copyright__: str = "(c) 2014 - 2026 Eric Mesa"
__email__: str = "ericsbinaryworld at gmail dot com"

import json
import logging

from logging_journald import JournaldLogHandler
from rich.logging import RichHandler

log = logging.getLogger("snapintime")
log.setLevel(logging.INFO)
RICH_FORMAT = logging.Formatter("%(message)s", "[%X]")
console_handler = RichHandler()
console_handler.setFormatter(RICH_FORMAT)
log.addHandler(console_handler)

class StructuredMessage:
    def __init__(self, message, /, **kwargs):
        self.message = message
        self.kwargs = kwargs

    def __str__(self):
        return f'{self.message} >>> {json.dumps(self.kwargs)}'

slog = logging.getLogger("snapintime")
slog.setLevel(logging.DEBUG)
if JournaldLogHandler.SOCKET_PATH.exists():
    slog.addHandler(JournaldLogHandler())
else:
    slog.addHandler(console_handler) # if no journald, just make it another console log

print(f"Using version {__version__}")
