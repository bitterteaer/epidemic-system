import socket
import requests
from configs import video_post_url

# 函数 gethostname() 返回当前正在执行 Python 的系统主机名
res = socket.gethostbyname(socket.gethostname())


def data_post(data_dict, url):
    response = requests.post(url,
                             data=data_dict,
                             files=None,
                             verify=False,
                             stream=True)
    print("data upload state: ", response.status_code)


def video_post(files, pic_type):
    response = requests.post(video_post_url,
                             data={"pic_type": pic_type},
                             files=files,
                             verify=False,
                             stream=True)
    print("picture upload state: ", response.status_code)


if __name__ == "__main__":
    pass
