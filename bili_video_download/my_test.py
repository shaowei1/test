class Infinite(object):
    suffix = '%(index)d:%(max)d'

    message = 'yangxinyue'
    index = 10
    max = 100

    def __getitem__(self, key):
        # print(key)

        return getattr(self, key, None)
        # return 1

    def update(self):
        # self.suffix = '%(index)d:%(max)d'
        #
        # self.message = 'yangxinyue'
        # self.index = 10
        # self.max = 100

        message = self.message % self
        suffix = self.suffix % self

        print(message)
        print(suffix)

    def mytest(self):
        print(self.index % 100)


if __name__ == '__main__':
    bar = Infinite()
    # print(bar.index)
    bar.update()
    # bar.mytest()
