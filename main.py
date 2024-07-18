import os
import time
from pathlib import Path

import requests as rq
import spotipy
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth

from timer import Timer

load_dotenv()

SCOPE = "user-read-playback-state"
REFRESH_RATE: float = float(os.getenv("REFRESH_RATE", 5))
COVER_SIZE: int = int(os.getenv("COVER_SIZE", 1))

OUTPUT_FORMAT: str = os.getenv("OUTPUT_FORMAT", '"{TITLE}" - {ARTIST} ({CURRENT}/{DURATION})')
OUTPUT_FOLDER: Path = Path(os.getenv("OUTPUT_FOLDER", "output"))
OUTPUT_FILE: Path = OUTPUT_FOLDER / (os.getenv("OUTPUT_FILE", "track.txt"))
OUTPUT_COVER: Path = OUTPUT_FOLDER / (os.getenv("OUTPUT_COVER", "cover.jpg"))


def ms_to_time(ms):
    return time.strftime("%M:%S", time.gmtime(ms / 1000))


def current_milli_time():
    return round(time.time() * 1000)


class Spotify:
    def __init__(self):
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=SCOPE))
        self.is_playing: bool = False
        self.title: str = None
        self.artist: str = None
        self.current: int = None
        self.duration: int = None
        self.last_time: int = None
        self.cover_link: str = None
        self.last_output: str = None
        self.last_cover_link: str = None

    def listen(self):
        fetcher = Timer(REFRESH_RATE, self.fetch_track)
        fetcher.start()

        while True:
            try:
                time.sleep(1)
                self.export_track()
            except KeyboardInterrupt:
                print("Exiting...")
                fetcher.cancel()
                break

    def fetch_track(self):
        print("Fetching...")
        track = self.sp.current_user_playing_track()
        self.is_playing = track is not None and track["is_playing"]
        self.save_track(track)

    def save_track(self, track):
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

    def export_track(self, no_save=False):
        if not self.is_playing:
            return
        current = self.current + (current_milli_time() - self.last_time) if self.is_playing else self.current
        output = OUTPUT_FORMAT.format(
            TITLE=self.title,
            ARTIST=self.artist,
            CURRENT=ms_to_time(current),
            DURATION=ms_to_time(self.duration),
        )

        if output == self.last_output:
            return
        self.last_output = output

        print(output)

        if no_save:
            return

        with open(OUTPUT_FILE, "w") as f:
            f.write(output)

        if self.last_cover_link != self.cover_link and self.cover_link != None:
          self.last_cover_link = self.cover_link

          with open(OUTPUT_COVER, "wb") as f:
              f.write(rq.get(self.cover_link).content)


if __name__ == "__main__":
    Spotify().listen()

# TODO:
# - [x] Try spotify api
# - [x] get current track info
# - [x] save track info to file
# - [x] download image
# - [x] Thread polling & progress calculation
# - [ ] progress bar ??
