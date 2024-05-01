import os
import time
from pathlib import Path

import requests as rq
import spotipy
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth

load_dotenv()

SCOPE = "user-read-playback-state"
REFRESH_RATE = int(os.getenv("REFRESH_RATE"))
COVER_SIZE = int(os.getenv("COVER_SIZE"))

OUTPUT_FORMAT = os.getenv("OUTPUT_FORMAT")
OUTPUT_FOLDER = os.getenv("OUTPUT_FOLDER")
OUTPUT_FILE = os.getenv("OUTPUT_FILE")
OUTPUT_COVER = os.getenv("OUTPUT_COVER")


def ms_to_time(ms):
    return time.strftime("%M:%S", time.gmtime(ms / 1000))


class Spotify:
    def __init__(self):
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=SCOPE))
        self.title: str = None
        self.artist: str = None
        self.current: int = None
        self.duration: int = None
        self.last_time: int = None
        self.cover_link: str = None

        self.last_output: str = None

    def listen(self):
        while True:
            track = self.sp.current_user_playing_track()
            if track is None or track["is_playing"] is False:
                print("No track playing")
            else:
                self.save_track(track)
                self.export_track()
            time.sleep(REFRESH_RATE)

    def save_track(self, track):
        self.title = track["item"]["name"]
        self.artist = ", ".join([artist["name"] for artist in track["item"]["artists"]])
        self.current = track["progress_ms"]
        self.duration = track["item"]["duration_ms"]
        self.last_time = track["timestamp"]
        self.cover_link = list(reversed(track["item"]["album"]["images"]))[COVER_SIZE]["url"]

    def export_track(self):
        output = OUTPUT_FORMAT.format(
            TITLE=self.title,
            ARTIST=self.artist,
            CURRENT=ms_to_time(self.current),
            DURATION=ms_to_time(self.duration),
        )

        if output == self.last_output:
            return
        self.last_output = output

        print(output)

        with open(Path(OUTPUT_FOLDER) / OUTPUT_FILE, "w") as f:
            f.write(output)

        with open(Path(OUTPUT_FOLDER) / OUTPUT_COVER, "wb") as f:
            f.write(rq.get(self.cover_link).content)


if __name__ == "__main__":
    Spotify().listen()

# TODO:
# - [x] Try spotify api
# - [x] get current track info
# - [x] save track info to file
# - [x] download image
# - [ ] progress bar ??
