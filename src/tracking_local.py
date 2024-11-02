import time

import requests as rq

from .constants import OUTPUT_COVER, OUTPUT_FILE
from .tracking import Tracking


class _LocalTracking(Tracking):
    def __init__(self):
        super().__init__()
        self.last_output: str = None

    def listen(self):
        while True:
            try:
                time.sleep(1)
                self.export_track()
            except KeyboardInterrupt:
                break

    def export_track(self):
        if not self.is_playing or self.last_output == self.output:
            return  # No export if not playing or no changes

        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write(self.output)
        self.last_output = self.output

        print(self.output)

        if self.cover_link is None or self.last_cover_link == self.cover_link:
            return
        self.last_cover_link = self.cover_link

        with open(OUTPUT_COVER, "wb") as f:
            f.write(rq.get(self.cover_link).content)


LocalTracking = _LocalTracking()  # Singleton instance for one tracking
