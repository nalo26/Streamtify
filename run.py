from src.constants import EXPORT_FORMAT
from src.tracking_local import LocalTracking
from src.tracking_server import ServerTracking
from src.utils import Format

if __name__ == "__main__":
    if EXPORT_FORMAT == Format.SERVER:
        ServerTracking.run()
    else:  # Format.LOCAL
        LocalTracking.run()
