import time
from threading import Event, Thread


class Timer:
    def __init__(self, interval, function, args=(), kwargs=None):
        self.interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs or {}
        self.running = Event()
        self.running.set()

    def start(self):
        def run():
            while self.running.is_set():
                self.function(*self.args, **self.kwargs)
                time.sleep(self.interval)

        self.thread = Thread(target=run)
        self.thread.start()

    def cancel(self):
        self.running.clear()
        self.thread.join()
