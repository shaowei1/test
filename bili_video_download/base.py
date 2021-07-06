from collections import deque
from datetime import timedelta
from math import ceil  # return the smallest integer >= x.
from sys import stderr  # None
from time import time

HIDE_CURSOR = '\x1b[?25l'  # hide cursor
SHOW_CURSOR = '\x1b[?25h'  # show cursor


class Infinite(object):
    file = stderr  # None
    sma_window = 10  # Simple Moving Average window
    check_tty = True
    hide_cursor = True

    def __init__(self, message, **kwargs):
        self.index = 0
        self.start_ts = time()
        self.avg = 0
        self._ts = self.start_ts
        self._xput = deque(maxlen=self.sma_window)
        for key, val in kwargs.items():
            setattr(self, key, val)  # self.key = val

        self._width = 0
        self.message = message

        if self.file and self.is_tty():
            if self.hide_cursor:
                print(HIDE_CURSOR, end='', file=self.file)
            print(self.message, end='', file=self.file)
            self.file.flush()

    def __getitem__(self, key):
        if key.startswith('_'):
            return None
        return getattr(self, key, None)

    @property
    def elapsed(self):
        return int(time() - self.start_ts)

    @property
    def elapsed_td(self):
        return timedelta(seconds=self.elapsed)

    def update_avg(self, n, dt):
        if n > 0:
            self._xput.append(dt / n)
            self.avg = sum(self._xput) / len(self._xput)

    def is_tty(self):
        return self.file.isatty() if self.check_tty else True

    def clearln(self):
        if self.file and self.is_tty():
            print('\r\x1b[K', end='', file=self.file)  # '\x1b[K'清除光标到行尾的内容

    def write(self, s):
        if self.file and self.is_tty():
            line = self.message + s.ljust(self._width)
            print('\r' + line, end='', file=self.file)
            self._width = max(self._width, len(s))
            self.file.flush()

    def writeln(self, line):
        # if self.file and self.is_tty():
        self.clearln()
        print(line, end='', file=self.file)
        self.file.flush()

    def next(self, n=1):
        now = time()
        dt = now - self._ts
        self.update_avg(n, dt)
        self._ts = now
        self.index = self.index + n
        self.update()

    def update(self):
        pass

    def start(self):
        pass

    def finish(self):
        if self.file and self.is_tty():
            print(file=self.file)
            if self.hide_cursor:
                print(SHOW_CURSOR, end='', file=self.file)

    def iter(self, it):
        with self:
            for x in it:
                yield x
                self.next()

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.finish()


class Progress(Infinite):
    def __init__(self, *args, **kwargs):
        super(Progress, self).__init__(*args, **kwargs)
        self.max = kwargs.get('max', 100)

    @property
    def eta(self):
        return int(ceil(self.avg * self.remaining))

    @property
    def eta_td(self):
        return timedelta(seconds=self.eta)  # 00:00:00

    @property
    def percent(self):
        return self.progress * 100

    @property
    def progress(self):
        return min(1, self.index / self.max)

    @property
    def remaining(self):
        return max(self.max - self.index, 0)

    def start(self):
        self.update()

    def goto(self, index):
        incr = index - self.index
        self.next(incr)

    def iter(self, it):
        try:
            self.max = len(it)
        except TypeError:
            pass

        with self:
            for x in it:
                yield x
                self.next()
