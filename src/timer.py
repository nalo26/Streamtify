import asyncio
from threading import Event, Thread
from typing import Callable


class Timer:
    def __init__(self, interval: float, function: Callable, args=(), kwargs=None):
        self.interval = interval
        self.function = function  # Can be sync or async
        self.args = args
        self.kwargs = kwargs or {}
        self._stop_event = Event()
        self._thread: Thread = None
        self._loop: asyncio.AbstractEventLoop = None

    def start(self):
        def target():
            self._loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self._loop)

            try:
                while not self._stop_event.is_set():
                    if asyncio.iscoroutinefunction(self.function):
                        self._loop.run_until_complete(self.function(*self.args, **self.kwargs))
                    else:
                        self.function(*self.args, **self.kwargs)

                    # Use sleep for simplicity
                    self._stop_event.wait(self.interval)
            finally:
                self._loop.close()

        self._thread = Thread(target=target, daemon=True)
        self._thread.start()

    def cancel(self):
        self._stop_event.set()
        if self._thread:
            self._thread.join(timeout=2.0)
