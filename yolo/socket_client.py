import socket
import random
import time
from configs import HOST, PORT, socket_or_post

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 定义socket类型，网络通信，TCP


def init_socket():
    # data = str(s.recv(1024), encoding='utf-8')  # 把接收的数据实例化
    # print(data)
    s.connect((HOST, PORT))

    while 1:
        cmd = str(random.randint(1, 100))
        s.send(bytes(cmd, encoding='utf-8'))  # 把命令发送给对端
        # data = s.recv(1024)  # 把接收的数据定义为变量
        time.sleep(0.01)
    s.close()  # 关闭连接


if __name__ == "__main__":
    init_socket()
