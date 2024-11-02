from flask import Flask, render_template
from flask_socketio import SocketIO

from .constants import SERVER_HOST, SERVER_PORT
from .timer import Timer
from .tracking import Tracking


class _ServerTracking(Tracking):
    def __init__(self):
        super().__init__()
        self.app = Flask(__name__)
        self.socket = SocketIO(self.app)

    def listen(self):
        export = Timer(1, self.export_track)
        export.start()
        self.app.run(SERVER_HOST, SERVER_PORT, debug=False)
        export.cancel()

    def export_track(self):
        with app.app_context():
            self.output = self.format_track()
            if not self.is_playing or self.last_output == self.output:
                return  # No export if not playing or no changes

            self.last_output = self.output
            data = {
                "title": self.title,
                "artist": self.artist,
                "output": self.output,
                "current": self.current,
                "duration": self.duration,
                "cover_link": self.cover_link,
            }
            self.socket.emit("update", data)


ServerTracking = _ServerTracking()  # Singleton instance for one tracking
_track = ServerTracking  # alias for simpler usage
app = _track.app


@app.route("/")
def render():
    return render_template("render.html.jinja", track=_track)


@app.route("/track")
def track():
    print(_track.output)
    return render_template("text.html.jinja", id="output", data=_track.output)


@app.route("/title")
def title():
    return render_template("text.html.jinja", id="title", data=_track.title)


@app.route("/artist")
def artist():
    return render_template("text.html.jinja", id="artist", data=_track.artist)


@app.route("/cover")
def cover():
    return render_template("image.html.jinja", id="cover", data=_track.cover_link)
