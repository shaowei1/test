#!/usr/bin/python3
from progress import ShowProcess

from socket import AF_INET, SOCK_STREAM, socket
import os
import sys  # Import the Modules
import re
import subprocess


class BiliBili(object):
    def __init__(self, url):
        # 创建套接字，构造request
        self.client = socket(AF_INET, SOCK_STREAM)

        match_obj1 = re.match('https://(.*\.com)/.*', url)
        host = match_obj1.group(1)
        print(host)
        self.client.connect((host, 80))

        match_obj2 = re.match(r'.*.com(.*)', url)
        path = match_obj2.group(1)
        request_line = "GET " + path + " HTTP/1.1\r\n"
        print(path)
        request_header = 'Host: {}\r\n'.format(host)
        request_header += 'Connection: close\r\n'
        request_header += 'Origin: https://www.bilibili.com\r\n'
        request_header += 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/69.0.3497.81 Chrome/69.0.3497.81 Safari/537.36\r\n'
        request_header += 'Accept: */*\r\n'
        request_header += 'Referer: https://www.bilibili.com/video/av27034325\r\n'
        request_header += 'Accept-Encoding: gzip, deflate, br\r\n'
        request_header += 'Accept-Language: en,zh;q=0.9,zh-CN;q=0.8\r\n'

        request_content = request_line + request_header + "\r\n"

        self.request_content = request_content.encode('utf-8')

    def handle_http(self, filename):
        # 发送http请求，接受响应，写入到filename中
        f = open(filename, 'ab')
        f.truncate()
        self.client.send(self.request_content)
        while True:
            recv_data = self.client.recv(1024)
            if recv_data:
                process_bar.show_process()

                f.write(recv_data)
            else:
                break
        f.close()
        self.client.close()

    @staticmethod
    def search_str_lines1(matching, filename):
        # search line number from file
        with open(filename, 'rt', encoding='latin-1') as f:
            for i, line in enumerate(f, 1):
                if matching in line:
                    print(i, line)
                    break
        return i

    @staticmethod
    def del_head(row, filename):
        # 删除响应行和响应体
        param1 = '1,' + str(row + 1) + 'd'
        # 调用系统命令sed -i '1,nd' filename, 从filename中，删除１到ｎ行
        os.system(''' sed -i {}  {} '''.format(param1, filename))

    # Prints usage if not appropriate length of arguments are provided
    @staticmethod
    def usage():
        print('[-] Usage1: ./bili.py [filename1] [url]')
        print('[-] Usage2: python3 bili.py [filename1] [url]')

    def run(self):
        # Check the arguments passed to the script
        print(len(sys.argv))
        if len(sys.argv) == 3:
            filename = sys.argv[1]
            try:
                if not os.path.isfile(filename):  # Check the File exists
                    print('[-] ' + filename + ' does not exist.')
                    if filename.endswith('.flv'):
                        os.system("touch {}".format(filename))
                    else:
                        file = filename.split('.')
                        filename = file[0] + '.flv'
                        os.system("touch {}".format(filename))
            except Exception as e:
                print("catch except: " + str(e))

            self.handle_http(filename)
            row = self.search_str_lines1("Accept-Ranges: bytes", filename)
            self.del_head(row, filename)
            exit()
        else:
            self.usage()


def main():
    url = sys.argv[2]
    bili = BiliBili(url=url)
    bili.run()


if __name__ == '__main__':
    max_steps = 100
    process_bar = ShowProcess(max_steps, 'OK')
    main()
