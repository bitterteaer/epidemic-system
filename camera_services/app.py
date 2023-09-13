import _thread
import queue
import time

import cv2
from flask import Flask, Response
# import json

app = Flask(__name__)

# 全局变量
frame_queue = None
camera_flag = None
source = 0


def open_camera():
    # yield "pass"
    global camera_flag
    global frame_queue
    global source

    # if camera_flag == 0:
    #     return
    camera_flag = 0
    frame_queue = queue.Queue(maxsize=3)

    # with open('../configs.json', 'r') as f:
    #     configs = json.load(f)
    # try:
    #     source = configs['camera']
    #     source = int(source)
    # except:
    #     pass

    cap = cv2.VideoCapture(source)
    # print(cap.get(5))
    print("open_camera", camera_flag)
    while camera_flag == 0:
        ret, frame = cap.read()
        # print(frame.shape)
        if not ret:
            break
        if frame_queue.full():
            frame_queue.get()  # 如果队列满了，删除最旧的帧
        frame_queue.put(frame)

    cap.release()
    frame_queue = None

    print("quit open_camera")
    return "success"


# @bp.route('/close_camera')
def close_camera():
    global camera_flag
    camera_flag = 1
    print("close_camera", camera_flag)

    return "success"


@app.route('/video_feed')
def video_feed():
    global camera_flag
    global frame_queue

    close_camera()
    time.sleep(0.5)
    # 创建线程
    try:
        _thread.start_new_thread(open_camera, ())
    except:
        print("Error: 无法启动线程")
    time.sleep(0.1)

    def cv2_stream():
        # cap = cv2.VideoCapture(camera_url)
        # print(camera_flag)
        while camera_flag == 0:
            # time.sleep(1)
            frame = frame_queue.get()
            # ret, frame = cap.read()
            ret, jpeg = cv2.imencode('.jpg', frame)
            data = jpeg.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + data + b'\r\n\r\n')

        # cap.release()
        print("cap quit")

    return Response(cv2_stream(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=4999
    )
