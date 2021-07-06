import requests
from bs4 import BeautifulSoup

r = requests.get("http://www.pythonscraping.com")
bs = BeautifulSoup(r.text, 'lxml')
image = bs.find("a", {"id": "logo"}).find("img")["src"]

ir = requests.get(image)
if ir.status_code == 200:
    open('logo.jpg', 'wb').write(ir.content)

'''
Ctrl-Z：该键是linux下面默认的挂起键（Suspend Key），当键入Ctrl-Z时，系统会将正在运行的程序挂起，然后放到后台，同时给出用户相关的job信息。此时，程序并没有真正的停止，用户可以通过使用fg、bg命令将job恢复到暂停前的上下文环境，并继续执行。

Ctrl-C：该键是linux下面默认的中断键（Interrupt Key），当键入Ctrl-C时，系统会发送一个中断信号给正在运行的程序和shell。具体的响应结果会根据程序的不同而不同。一些程序在收到这个信号后，会立即结束并推出程序，一些程序可能会忽略这个中断信号，还有一些程序在接受到这个信号后，会采取一些其他的动作（Action）。当shell接受到这个中断信号的时候，它会返回到提示界面，并等待下一个命令。

Ctrl-D：该键是Linux下面标准输入输出的EOF。在使用标准输入输出的设备中，遇到该符号，会认为读到了文件的末尾，因此结束输入或输出。

作者：Yvanna_15
链接：https://www.jianshu.com/p/a4ce7c79f54a
來源：简书
简书著作权归作者所有，任何形式的转载都请联系作者获得授权并注明出处。
'''

'''
from urllib.request import urlretrieve

import requests
from bs4 import BeautifulSoup

r = requests.get("http://www.pythonscraping.com")
bs = BeautifulSoup(r.text)
image = bs.find("a", {"id": "logo"}).find("img")["src"]

urlretrieve(image, "logo.jpg")

# ir = requests.get(image, stream=True)
# if ir.status_code == 200:
#     with open('logo.jpg', 'wb') as f:
#         for chunk in ir:
#             f.write(chunk)
'''

'''
import re, requests

r = requests.get("http://www.pythonscraping.com")
p = re.compile(r'<a[^>]*?id="logo"[^<]*?<img[^>]*?src="([^"]*)')
image = p.findall(r.text)[0]
ir = requests.get(image)
sz = open('logo.jpg', 'wb').write(ir.content)
print('logo.jpg', sz,'bytes')
'''
