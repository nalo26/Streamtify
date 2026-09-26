import base64
import hashlib
from collections import OrderedDict
from datetime import datetime

from winsdk.windows.media.control import GlobalSystemMediaTransportControlsSession as SMTCSession
from winsdk.windows.media.control import GlobalSystemMediaTransportControlsSessionManager as SMTCManager
from winsdk.windows.storage.streams import DataReader

from .constants import CONSOLE_ECHO, MAX_CACHE_SIZE, OUTPUT_FORMAT, REFRESH_RATE, SERVER_EXPORT, SMTC_TARGET_APP
from .timer import Timer
from .utils import current_milli_time, ms_to_time


# https://github.com/nuttylmao/smtc-bridge/blob/main/smtc-bridge.pyw
class Tracking:
    def __init__(self):
        self.manager: SMTCManager = None
        self.is_playing: bool = False
        self.title: str = None
        self.artist: str = None
        self.current: int = None
        self.duration: int = None
        self.last_time: int = None
        self.output: str = None
        self.last_output: str = None
        self.cover_link: str = None
        self.last_cover_link: str = None

        self.thumb_cache = OrderedDict()

    async def run(self):
        self.manager = await SMTCManager.request_async()
        print(f"Fetching SMTC track every {REFRESH_RATE}s,")
        print(f"exporting in {'Server' if SERVER_EXPORT else 'Local'} mode [Ctrl+C to exit]")
        self.fetcher = Timer(REFRESH_RATE, self.fetch_track)
        self.fetcher.start()

        self.listen()  # Childs will implement this
        print("Exiting...")
        self.fetcher.cancel()

    async def fetch_track(self):
        for session in self.manager.get_sessions():
            if session.source_app_user_model_id.lower() != SMTC_TARGET_APP.lower():
                continue

            last_update = session.get_timeline_properties().last_updated_time.replace(tzinfo=None)
            self.is_playing = (last_update - datetime.now()).total_seconds() < 2
            await self.save_track(session)

    async def save_track(self, session: SMTCSession):
        if not self.is_playing:
            return

        # raw_playback = session.get_playback_info()
        raw_timeline = session.get_timeline_properties()
        raw_media = await session.try_get_media_properties_async()
        self.last_time = current_milli_time()

        self.title = raw_media.title if raw_media else "Unknown"
        self.artist = raw_media.artist if raw_media else "Unknown"
        self.current = int(raw_timeline.position.total_seconds() * 1000) if raw_timeline.position else 0
        self.duration = int(raw_timeline.end_time.total_seconds() * 1000) if raw_timeline.end_time else 0
        self.cover_link = await self.extract_cover(raw_media.thumbnail)

    async def extract_cover(self, thumbnail) -> str:
        thumb_url = None
        try:
            stream = await thumbnail.open_read_async()
            reader = DataReader(stream.get_input_stream_at(0))
            await reader.load_async(stream.size)
            buffer = bytearray(stream.size)
            reader.read_bytes(buffer)

            img_hash = hashlib.md5(buffer).hexdigest()
            if img_hash in self.thumb_cache:
                self.thumb_cache.move_to_end(img_hash)
                thumb_url = self.thumb_cache[img_hash]
            else:
                # Convert raw Windows bytes straight to Base64
                encoded_img = base64.b64encode(bytes(buffer)).decode("utf-8")
                thumb_url = f"data:image/jpeg;base64,{encoded_img}"

                self.thumb_cache[img_hash] = thumb_url
                if len(self.thumb_cache) > MAX_CACHE_SIZE:
                    self.thumb_cache.popitem(last=False)

        except Exception:
            thumb_url = "static/nocover.jpg"

        return thumb_url

    def format_track(self):
        if not self.is_playing:
            return
        format = OUTPUT_FORMAT
        if self.artist in ("", None):
            format = format.replace("{ARTIST} - ", "")
            format = format.replace(" - {ARTIST}", "")
        current = self.current + (current_milli_time() - self.last_time) if self.is_playing else self.current
        if current > self.duration:
            current = self.duration
        formated = format.format(
            TITLE=self.title,
            ARTIST=self.artist,
            CURRENT=ms_to_time(current),
            DURATION=ms_to_time(self.duration),
        )
        if CONSOLE_ECHO and self.is_playing and self.last_output != formated:
            print(formated)
        return formated

    def listen(self):
        raise NotImplementedError

    def export_track(self):
        raise NotImplementedError
