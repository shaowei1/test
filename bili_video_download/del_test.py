import os


def del_head(row, filename):
    os.system(''' sed -i {}  {} '''.format(row, filename))


if __name__ == '__main__':
    row = '1' + 'd'
    filename = '1.txt'
    del_head(row, filename)
