from functools import partial
from threading import Timer

from flask_socketio import SocketIO

import app


class SocketTimer(object):

    def __init__(self, interval_in_seconds, function, args=None, kwargs=None):
        """
        Runs the function at a specified interval_in_seconds with given arguments.
        """
        if kwargs is None:
            kwargs = {}
        if args is None:
            args = []

        self.interval = interval_in_seconds
        self.function = partial(function, *args, **kwargs)
        self.running = False
        self._timer = None

    def __call__(self):
        """
        Handler function for calling the partial and continuting.
        """
        self.running = False  # mark not running
        self.start()  # reset the timer for the next go
        self.function()  # call the partial function

    def start(self):
        """
        Starts the interval and lets it run.
        """
        if self.running:
            # Don't start if we're running!
            return

            # Create the timer object, start and set state.
        self._timer = Timer(self.interval, self)
        self._timer.start()
        self.running = True

    def stop(self):
        """
        Cancel the interval (no more function calls).
        """
        if self._timer:
            self._timer.cancel()
        self.running = False
        self._timer = None


if __name__ == "__main__":
    import time

    question_count = 0
    socketio = SocketIO(app, session=False)


    def clock(start, qc):
        """
        Prints out the elapsed time when called from start.
        """
        print("elapsed")
        socketio.emit()

        if qc == 9:
            interval.stop()


    # Create an interval.
    interval = SocketTimer(10, clock, args=[time.time(), question_count])
    print("Starting Interval, press CTRL+C to stop.")
    interval.start()

    while True:
        try:
            time.sleep(0.1)
        except KeyboardInterrupt:
            print("Shutting down interval ...")
            interval.stop()
            break
