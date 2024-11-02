from flask import Flask

from .constants import SERVER_HOST, SERVER_PORT
from .tracking import Tracking

app = Flask(__name__)


class _ServerTracking(Tracking):
    def __init__(self):
        super().__init__()

    def listen(self):
        app.run(SERVER_HOST, SERVER_PORT)


ServerTracking = _ServerTracking()  # Singleton instance for one tracking
track = ServerTracking  # alias for simpler usage


@app.route("/")
def hello_world():
    print(track.output)
    return track.output
