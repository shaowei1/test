import urllib
import os
import requests
import re
import gevent
from gevent import monkey

# 打补丁，让gevent框架识别耗时操作，比如：time.sleep，网络请求延时
monkey.patch_all()


def down_html(url):
    start_url = 'https://wallscollection.net/g-l/images-of-beautiful-girl.html'
    req = requests.get(url=start_url)
    print(req.text)


def match_url(html):
    with open('html.txt', 'r') as f:
        data = f.read()
    url_list = re.findall(r'http://wallscollection.net/wp-content/uploads.*?.jpg', data)
    collections = set()
    for tem in url_list:
        collections.add(tem)
    print(collections)


def down_image(col):
    x = 0
    for img_url in list(col):
        try:
            ir = requests.get(img_url)
            if ir.status_code == 200:
                open('/home/yue/PycharmProjects/web_server/image/%s.jpg' % x, 'wb').write(ir.content)
            x += 1
        except Exception as e:
            print("{} catch {} error".format(img_url, e))


def yield_down(x, y):
    a = x
    for t in col[x:y]:
        # os.system('''wget -O %s.jpg %s''' % (a, t))
        # os.system('''wget -O %s.jpg %s''' % (t.rsplit('/')[-1], t))
        network_file = urllib.request.urlopen(t)
        with open("{}.jpg".format(a), 'wb') as f:
            while True:
                img_data = network_file.read(1024)
                if img_data:
                    f.write(img_data)
                else:
                    break
        a += 1


def download_img(img_url, img_name):
    try:
        network_file = urllib.request.urlopen(img_url)
        with open(img_name, 'wb') as img_file:
            while True:
                img_data = network_file.read(1024)
                if img_data:
                    img_file.read(img_data)
                else:
                    break
    except Exception as e:
        print("fine exception", e)
    else:
        print("200 OK")


import time

if __name__ == '__main__':
    col = {'http://wallscollection.net/wp-content/uploads/2017/02/Images-Of-Beautiful-Girl-HD-Collection.jpg',
           'http://wallscollection.net/wp-content/uploads/2017/02/Images-Of-Beautiful-Girl-For-Desktop-.jpg',
           'http://wallscollection.net/wp-content/uploads/2017/02/Images-Of-Beautiful-Girl-Photos.jpg',
           'http://wallscollection.net/wp-content/uploads/2017/02/Images-Of-Beautiful-Girl-For-Laptop.jpg',
           'http://wallscollection.net/wp-content/uploads/2017/02/Images-Of-Beautiful-Girl-Download-For-Free.jpg',
           'http://wallscollection.net/wp-content/uploads/2017/02/Images-Of-Beautiful-Girl-In-Best-Resolutions.jpg',
           'http://wallscollection.net/wp-content/uploads/2017/02/Awesome-Beautiful-Images-Of-Beautiful-Girl-.jpg',
           'http://wallscollection.net/wp-content/uploads/2017/02/Images-Of-Beautiful-Girl-Photo-Collection.jpg',
           'http://wallscollection.net/wp-content/uploads/2017/02/Images-Of-Beautiful-Girl-Great-Collection.jpg',
           'http://wallscollection.net/wp-content/uploads/2017/02/Images-Of-Beautiful-Girl-In-High-Quality.jpg',
           'http://wallscollection.net/wp-content/uploads/2017/02/Images-Of-Beautiful-Girl-1920x1080.jpg',
           'http://wallscollection.net/wp-content/uploads/2017/02/New-Images-Of-Beautiful-Girl-.jpg',
           'http://wallscollection.net/wp-content/uploads/2017/02/Images-Of-Beautiful-Girl-Compatible.jpg',
           'http://wallscollection.net/wp-content/uploads/2017/02/Images-Of-Beautiful-Girl-Widescreen.jpg',
           'http://wallscollection.net/wp-content/uploads/2017/02/Images-Of-Beautiful-Girl-4K-Pack.jpg',
           'http://wallscollection.net/wp-content/uploads/2017/02/Amazing-Images-Of-Beautiful-Girl-.jpg',
           'http://wallscollection.net/wp-content/uploads/2017/02/Images-Of-Beautiful-Girl-in-HD-Resolution.jpg',
           'http://wallscollection.net/wp-content/uploads/2017/02/Images-Of-Beautiful-Girl-Free-Download.jpg',
           'http://wallscollection.net/wp-content/uploads/2017/02/Images-Of-Beautiful-Girl-In-High-Definition-.jpg',
           'http://wallscollection.net/wp-content/uploads/2017/02/Ultra-HD-Images-Of-Beautiful-Girl.jpg',
           'http://wallscollection.net/wp-content/uploads/2017/02/High-Quality-Images-Of-Beautiful-Girl-.jpg',
           'http://wallscollection.net/wp-content/uploads/2017/02/Images-Of-Beautiful-Girl-Gallery-.jpg',
           'http://wallscollection.net/wp-content/uploads/2017/02/Images-Of-Beautiful-Girl-Mobile-Compatible.jpg',
           'http://wallscollection.net/wp-content/uploads/2017/02/Top-Images-Of-Beautiful-Girl-.jpg',
           'http://wallscollection.net/wp-content/uploads/2017/02/Images-Of-Beautiful-Girl-HD-.jpg',
           'http://wallscollection.net/wp-content/uploads/2017/02/Images-Of-Beautiful-Girl-HD.jpg',
           'http://wallscollection.net/wp-content/uploads/2017/02/Images-Of-Beautiful-Girl-For-Background-.jpg',
           'http://wallscollection.net/wp-content/uploads/2017/02/Wide-Images-Of-Beautiful-Girl-.jpg'}
    col = list(col)
    length = len(col)
    print(length)
    os.chdir('image')
    # g1 = gevent.spawn(yield_down, 0, 9)
    # g2 = gevent.spawn(yield_down, 9, 19)
    # g3 = gevent.spawn(yield_down, 19, 27)
    g = [None] * length
    for i in range(length):
        g[i] = gevent.spawn(download_img, col[i], "{}.jpg".format(i))
    gevent.joinall(g)
