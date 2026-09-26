import asyncio

from src.constants import EXPORT_FORMAT
from src.tracking_local import LocalTracking
from src.tracking_server import ServerTracking
from src.utils import Format

if __name__ == "__main__":
    func = ServerTracking.run if EXPORT_FORMAT == Format.SERVER else LocalTracking.run
    asyncio.run(func())
