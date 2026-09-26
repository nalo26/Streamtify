from pathlib import Path

from config import config

_config_smtc = config.get("smtc", {})
SMTC_TARGET_APP: str = _config_smtc.get("target_app", "")
MAX_CACHE_SIZE: int = _config_smtc.get("thumbnail_cache_size", 50)
REFRESH_RATE: float = _config_smtc.get("refresh_rate", 1)

_config_global = config.get("global", {})
CONSOLE_ECHO: bool = _config_global.get("console_echo", False)
OUTPUT_FORMAT: str = _config_global.get("output_format", '"{TITLE}" - {ARTIST} ({CURRENT}/{DURATION})')
SERVER_EXPORT: bool = _config_global.get("server_export", False)

_config_local = config.get("local_export", {})
OUTPUT_FOLDER: Path = Path(_config_local.get("output_folder", "output"))
OUTPUT_FILE: Path = OUTPUT_FOLDER / (_config_local.get("output_file", "track.txt"))
OUTPUT_COVER: Path = OUTPUT_FOLDER / (_config_local.get("output_cover", "cover.jpg"))

_config_server = config.get("server_export", {})
SERVER_HOST: str = _config_server.get("host", "localhost")
SERVER_PORT: int = _config_server.get("port", 16053)
