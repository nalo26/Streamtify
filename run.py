import asyncio

from src.constants import SERVER_EXPORT
from src.tracking_local import LocalTracking
from src.tracking_server import ServerTracking

if __name__ == "__main__":
    func = ServerTracking.run if SERVER_EXPORT else LocalTracking.run
    asyncio.run(func())
