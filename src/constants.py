import os
from pathlib import Path

from dotenv import load_dotenv

from .utils import Format

load_dotenv()

SCOPE = "user-read-playback-state"
REFRESH_RATE: float = float(os.getenv("REFRESH_RATE", 5))
COVER_SIZE: int = int(os.getenv("COVER_SIZE", 1))

OUTPUT_FORMAT: str = os.getenv("OUTPUT_FORMAT", '"{TITLE}" - {ARTIST} ({CURRENT}/{DURATION})')
EXPORT_FORMAT: Format = Format(int(os.getenv("EXPORT_FORMAT", 0)))

OUTPUT_FOLDER: Path = Path(os.getenv("OUTPUT_FOLDER", "output"))
OUTPUT_FILE: Path = OUTPUT_FOLDER / (os.getenv("OUTPUT_FILE", "track.txt"))
OUTPUT_COVER: Path = OUTPUT_FOLDER / (os.getenv("OUTPUT_COVER", "cover.jpg"))

SERVER_HOST: str = os.getenv("SERVER_HOST", "localhost")
SERVER_PORT: int = int(os.getenv("SERVER_PORT", 16053))
