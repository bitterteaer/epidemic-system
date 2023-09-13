import os
import time

import numpy as np
import requests

import objtracker
from exts import passers_by_requests_post, video_post
from objdetector import Detector
import cv2

from pydub import AudioSegment
from pydub.playback import play

from flask import Flask, Response, request

from urls import host_ip

app = Flask(__name__)


def run(VIDEO_PATH):
    # 根据视频尺寸，填充供撞线计算使用的polygon
    width = 1920
    height = 1080
    mask_image_temp = np.zeros((height, width), dtype=np.uint8)

    # 用于记录轨迹信息
    pts = {}

    # 填充第一个撞线polygon（蓝色）
    list_pts_blue = [[204, 305], [227, 431], [605, 522], [1101, 464], [1900, 601], [1902, 495], [1125, 379], [604, 437],
                     [299, 375], [267, 289]]
    ndarray_pts_blue = np.array(list_pts_blue, np.int32)
    polygon_blue_value_1 = cv2.fillPoly(mask_image_temp, [ndarray_pts_blue], color=1)
    polygon_blue_value_1 = polygon_blue_value_1[:, :, np.newaxis]

    # 填充第二个撞线polygon（黄色）
    mask_image_temp = np.zeros((height, width), dtype=np.uint8)
    list_pts_yellow = [[181, 305], [207, 442], [603, 544], [1107, 485], [1898, 625], [1893, 701], [1101, 568],
                       [594, 637], [118, 483], [109, 303]]
    ndarray_pts_yellow = np.array(list_pts_yellow, np.int32)
    polygon_yellow_value_2 = cv2.fillPoly(mask_image_temp, [ndarray_pts_yellow], color=2)
    polygon_yellow_value_2 = polygon_yellow_value_2[:, :, np.newaxis]

    # 撞线检测用的mask，包含2个polygon，（值范围 0、1、2），供撞线计算使用
    polygon_mask_blue_and_yellow = polygon_blue_value_1 + polygon_yellow_value_2

    # 缩小尺寸，1920x1080->960x540
    polygon_mask_blue_and_yellow = cv2.resize(polygon_mask_blue_and_yellow, (width // 2, height // 2))

    # 蓝 色盘 b,g,r
    blue_color_plate = [255, 0, 0]
    # 蓝 polygon图片
    blue_image = np.array(polygon_blue_value_1 * blue_color_plate, np.uint8)

    # 黄 色盘
    yellow_color_plate = [0, 255, 255]
    # 黄 polygon图片
    yellow_image = np.array(polygon_yellow_value_2 * yellow_color_plate, np.uint8)

    # 彩色图片（值范围 0-255）
    color_polygons_image = blue_image + yellow_image

    # 缩小尺寸，1920x1080->960x540
    color_polygons_image = cv2.resize(color_polygons_image, (width // 2, height // 2))

    # list 与蓝色polygon重叠
    list_overlapping_blue_polygon = []

    # list 与黄色polygon重叠
    list_overlapping_yellow_polygon = []

    # 下行数量
    down_count = 0
    # 上行数量
    up_count = 0

    font_draw_number = cv2.FONT_HERSHEY_SIMPLEX
    draw_text_postion = (int((width / 2) * 0.01), int((height / 2) * 0.05))

    # 实例化yolov5检测器
    detector = Detector()

    # 打开视频
    capture = cv2.VideoCapture(VIDEO_PATH)

    # song = AudioSegment.from_wav("程序已经启动.wav")
    # play(song)
    # os.system("mpg123 程序已经启动.mp3")
    # try:
    #     _thread.start_new_thread(os.system, ("mpg123 程序已经启动.mp3",))
    # except:
    #     print("Error: 无法启动线程")

    # speak_old_time = time.time()
    old_time = time.time()
    while True:
        # 读取每帧图片
        _, im = capture.read()
        if im is None:
            break

        # 缩小尺寸，1920x1080->960x540
        im = cv2.resize(im, (width // 2, height // 2))

        list_bboxs = []
        # 更新跟踪器
        output_image_frame, list_bboxs = objtracker.update(detector, im)
        # print(list_bboxs)
        # 输出图片
        output_image_frame = cv2.add(output_image_frame, color_polygons_image)

        if len(list_bboxs) > 0:
            # ----------------------判断撞线----------------------
            for item_bbox in list_bboxs:
                # print(item_bbox)
                x1, y1, x2, y2, _, track_id = item_bbox
                # 撞线检测点，(x1，y1)，y方向偏移比例 0.0~1.0
                y1_offset = int(y1 + ((y2 - y1) * 0.5))
                x1_offset = int(x1 + ((x2 - x1) * 0.5))
                # 撞线的点
                y = y1_offset
                x = x1_offset

                # 然后每检测出一个预测框，就将中心点加入队列
                center = (x, y)
                if track_id in pts:
                    pts[track_id].append(center)
                else:
                    pts[track_id] = []
                    pts[track_id].append(center)

                thickness = 2
                cv2.circle(output_image_frame, (center), 1, [255, 255, 255], thickness)

                for j in range(1, len(pts[track_id])):
                    if pts[track_id][j - 1] is None or pts[track_id][j] is None:
                        continue
                    cv2.line(output_image_frame, (pts[track_id][j - 1]), (pts[track_id][j]), [255, 255, 255], thickness)

                if polygon_mask_blue_and_yellow[y, x] == 1:
                    # 如果撞 蓝polygon
                    if track_id not in list_overlapping_blue_polygon:
                        list_overlapping_blue_polygon.append(track_id)
                    # 判断 黄polygon list里是否有此 track_id
                    # 有此track_id，则认为是 UP (上行)方向
                    if track_id in list_overlapping_yellow_polygon:
                        # 上行+1
                        up_count += 1
                        # TODO print('up count:', up_count, ', up id:', list_overlapping_yellow_polygon)
                        print('up count:', up_count, ', up id:', list_overlapping_yellow_polygon)
                        # try:
                        #     passers_by_requests_post({
                        #         'up_or_down': 'up',
                        #         'count': down_count,
                        #         'id': list_overlapping_blue_polygon
                        #     })
                        # except:
                        #     print("无法连接到服务器")
                        # 删除 黄polygon list 中的此id
                        list_overlapping_yellow_polygon.remove(track_id)

                elif polygon_mask_blue_and_yellow[y, x] == 2:
                    # 如果撞 黄polygon
                    if track_id not in list_overlapping_yellow_polygon:
                        list_overlapping_yellow_polygon.append(track_id)
                    # 判断 蓝polygon list 里是否有此 track_id
                    # 有此 track_id，则 认为是 DOWN（下行）方向
                    if track_id in list_overlapping_blue_polygon:
                        # 下行+1
                        down_count += 1
                        # TODO print('down count:', down_count, ', down id:', list_overlapping_blue_polygon)
                        print('down count:', down_count, ', down id:', list_overlapping_blue_polygon)
                        # try:
                        #     passers_by_requests_post({
                        #         'up_or_down': 'down',
                        #         'count': down_count,
                        #         'id': list_overlapping_blue_polygon
                        #     })
                        # except:
                        #     print("无法连接到服务器")
                        # 删除 蓝polygon list 中的此id
                        list_overlapping_blue_polygon.remove(track_id)
            # ----------------------清除无用id----------------------
            list_overlapping_all = list_overlapping_yellow_polygon + list_overlapping_blue_polygon
            for id1 in list_overlapping_all:
                is_found = False
                for _, _, _, _, _, bbox_id in list_bboxs:
                    if bbox_id == id1:
                        is_found = True
                if not is_found:
                    # 如果没找到，删除id
                    if id1 in list_overlapping_yellow_polygon:
                        list_overlapping_yellow_polygon.remove(id1)

                    if id1 in list_overlapping_blue_polygon:
                        list_overlapping_blue_polygon.remove(id1)
            list_overlapping_all.clear()
            # 清空list
            list_bboxs.clear()
        else:
            # 如果图像中没有任何的bbox，则清空list
            list_overlapping_blue_polygon.clear()
            list_overlapping_yellow_polygon.clear()

        # 输出计数信息
        text_draw = 'DOWN: ' + str(down_count) + \
                    ' , UP: ' + str(up_count)
        output_image_frame = cv2.putText(img=output_image_frame, text=text_draw,
                                         org=draw_text_postion,
                                         fontFace=font_draw_number,
                                         fontScale=0.75, color=(0, 0, 255), thickness=2)
        # TODO send data
        res_dict = {"down_count": down_count, "up_count": up_count}
        print("send data:", res_dict)
        response = requests.post(f"{host_ip}/api/passers_by/set_data",
                                 data=res_dict,
                                 files=None,
                                 verify=False,
                                 stream=True)
        print("data upload state: ", response.status_code)

        # cv2.imshow('Counting Demo', output_image_frame)
        # cv2.waitKey(1)
        # TODO 上传图片到服务器
        if time.time() - old_time > 5:
            old_time = time.time()
            img_path = os.path.join(os.getcwd(), "results", "result.png")
            print('img_path:', img_path)
            cv2.imwrite(img_path, output_image_frame)
            files = {'file': open(img_path, 'rb')}
            # video_post(files, "mask")
            response = requests.post(f"{host_ip}/api/capture/save_picture_cut",
                                     data={"pic_type": 'deepsort_person'},
                                     files=files,
                                     verify=False,
                                     stream=True)
            print("picture upload state: ", response.status_code)

        # TODO stream results
        ret, jpeg = cv2.imencode('.jpg', output_image_frame)
        frame = jpeg.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

        # if time.time() - old_time > 10:
        #     old_time = time.time()
        #     img_path = os.path.join(os.getcwd(), "result.png")
        #     # cv2.imwrite(img_path, cv2.resize(output_image_frame, (160, 160)))
        #     cv2.imwrite(img_path, output_image_frame)
        #     files = {'file': open(img_path, 'rb')}
        #     try:
        #         status_ = video_post(files)
        #         # print(status_)
        #     except:
        #         print('无法连接到服务器')

    capture.release()
    cv2.destroyAllWindows()


@app.route("/person")
def person():
    realtime = request.args.get("realtime")
    print("realtime:", realtime)
    if realtime == "true":
        return Response(run(0), mimetype='multipart/x-mixed-replace; boundary=frame')
    else:
        return Response(run("video/test_person.mp4"), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    # run("video/test_person.mp4")
    app.run(
        port=5002,
        host='0.0.0.0'
    )
