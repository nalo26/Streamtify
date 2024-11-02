import spotipy
from spotipy.oauth2 import SpotifyOAuth

from .constants import CONSOLE_ECHO, COVER_SIZE, EXPORT_FORMAT, OUTPUT_FORMAT, REFRESH_RATE, SCOPE
from .timer import Timer
from .utils import current_milli_time, ms_to_time


class Tracking:
    def __init__(self):
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=SCOPE))
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

    def run(self):
        print(f"Fetching Spotify track every {REFRESH_RATE}s,")
        print(f"exporting in {EXPORT_FORMAT.name} mode [Ctrl+C to exit]")
        self.fetcher = Timer(REFRESH_RATE, self.fetch_track)
        self.fetcher.start()

        self.listen()  # Childs will implement this
        print("Exiting...")
        self.fetcher.cancel()

    def fetch_track(self):
        track = self.sp.current_user_playing_track()
        self.is_playing = track is not None and track["is_playing"]
        self.save_track(track)

    def save_track(self, track: dict):
        if not self.is_playing:
            return
        song = track["item"]
        self.title = song["name"]
        self.artist = ", ".join([artist["name"] for artist in song["artists"]])
        self.current = track["progress_ms"]
        self.duration = song["duration_ms"]
        if len(list(reversed(song["album"]["images"]))) > COVER_SIZE:
            self.cover_link = list(reversed(song["album"]["images"]))[COVER_SIZE]["url"]

        self.last_time = current_milli_time()

    def format_track(self):
        if not self.is_playing:
            return
        current = self.current + (current_milli_time() - self.last_time) if self.is_playing else self.current
        if current > self.duration:
            current = self.duration
        formated = OUTPUT_FORMAT.format(
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
