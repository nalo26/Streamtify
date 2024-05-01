import os
import time

import spotipy
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth

SCOPE = "user-read-playback-state"
REFRESH_RATE = os.getenv("REFRESH_RATE")


def ms_to_time(ms):
    return time.strftime("%M:%S", time.gmtime(ms / 1000))


class Spotify:
    def __init__(self):
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=SCOPE))

    def listen(self):
        while True:
            track = self.sp.current_user_playing_track()
            if track is None or track["is_playing"] is False:
                print("No track playing")
            else:
                self.print_track(track)
            time.sleep(REFRESH_RATE)

    def print_track(self, track):
        print(
            '"{title}" - {artist} ({current}/{duration})'.format(
                title=track["item"]["name"],
                artist=", ".join([artist["name"] for artist in track["item"]["artists"]]),
                current=ms_to_time(track["progress_ms"]),
                duration=ms_to_time(track["item"]["duration_ms"]),
            )
        )


if __name__ == "__main__":
    load_dotenv()
    Spotify().listen()

# TODO:
# - [x] Try spotify api
# - [x] get current track info
# - [ ] save track info to file
# - [ ] download image
# - [ ] progress bar ??
