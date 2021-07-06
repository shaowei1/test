from __future__ import unicode_literals
import time
from base import Progress


class Bar(Progress):
    width = 32
    suffix = '%(index)d:%(max)d'
    bar_prefix = ' |'
    bar_suffix = '| '
    empty_fill = ' '
    fill = '#'

    def update(self):
        filled_length = int(self.width * self.progress)
        empty_length = self.width - filled_length

        message = self.message % self

        bar = self.fill * filled_length
        empty = self.empty_fill * empty_length
        suffix = self.suffix % self
        # print(type(suffix))
        # % 用于格式化赋值
        # %(index)d%(max)d  %  self.index=1 , self.max=20
        line = ''.join([message, self.bar_prefix, bar, empty, self.bar_suffix, suffix])
        self.writeln(line)


def work(s):
    time.sleep(s)


if __name__ == '__main__':

    bar = Bar("message", max=20)
    for i in range(20):
        # do some work
        work(0.1)
        bar.next()
    bar.finish()
