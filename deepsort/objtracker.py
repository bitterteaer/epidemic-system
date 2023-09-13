import os
import time

from deep_sort.utils.parser import get_config
from deep_sort.deep_sort import DeepSort
import torch
import cv2
import numpy as np

from exts import capture_requests_post, group_requests_post

from pydub import AudioSegment
from pydub.playback import play

cfg = get_config()
cfg.merge_from_file("deep_sort/configs/deep_sort.yaml")
deepsort = DeepSort(cfg.DEEPSORT.REID_CKPT,
                    max_dist=cfg.DEEPSORT.MAX_DIST, min_confidence=cfg.DEEPSORT.MIN_CONFIDENCE,
                    nms_max_overlap=cfg.DEEPSORT.NMS_MAX_OVERLAP, max_iou_distance=cfg.DEEPSORT.MAX_IOU_DISTANCE,
                    max_age=cfg.DEEPSORT.MAX_AGE, n_init=cfg.DEEPSORT.N_INIT, nn_budget=cfg.DEEPSORT.NN_BUDGET,
                    use_cuda=True)


def plot_bboxes(image, bboxes, line_thickness=None):
    # Plots one bounding box on image img
    tl = line_thickness or round(
        0.002 * (image.shape[0] + image.shape[1]) / 2) + 1  # line/font thickness
    list_pts = []
    point_radius = 4

    for (x1, y1, x2, y2, cls_id, pos_id) in bboxes:
        if cls_id in ['smoke', 'phone', 'eat']:
            color = (0, 0, 255)
        else:
            color = (0, 255, 0)
        if cls_id == 'eat':
            cls_id = 'eat-drink'

        # check whether hit line 
        check_point_x = x1
        check_point_y = int(y1 + ((y2 - y1) * 0.6))

        c1, c2 = (x1, y1), (x2, y2)
        cv2.rectangle(image, c1, c2, color, thickness=tl, lineType=cv2.LINE_AA)
        tf = max(tl - 1, 1)  # font thickness
        t_size = cv2.getTextSize(cls_id, 0, fontScale=tl / 3, thickness=tf)[0]
        c2 = c1[0] + t_size[0], c1[1] - t_size[1] - 3
        cv2.rectangle(image, c1, c2, color, -1, cv2.LINE_AA)  # filled
        cv2.putText(image, '{} ID-{}'.format(cls_id, pos_id), (c1[0], c1[1] - 2), 0, tl / 3,
                    [225, 255, 255], thickness=tf, lineType=cv2.LINE_AA)

        list_pts.append([check_point_x - point_radius, check_point_y - point_radius])
        list_pts.append([check_point_x - point_radius, check_point_y + point_radius])
        list_pts.append([check_point_x + point_radius, check_point_y + point_radius])
        list_pts.append([check_point_x + point_radius, check_point_y - point_radius])

        ndarray_pts = np.array(list_pts, np.int32)
        cv2.fillPoly(image, [ndarray_pts], color=(0, 0, 255))
        list_pts.clear()
    return image


def update(target_detector, image):
    _, bboxes = target_detector.detect(image)
    # print(bboxes, end="\n----------\n")
    # print(bboxes)
    bbox_xywh = []
    confs = []
    label = []
    bboxes2draw = []
    if len(bboxes):
        # Adapt detections to deep sort input format
        # print(bboxes)
        # print("bboxes", bboxes, end="\n\n")
        for x1, y1, x2, y2, _, conf in bboxes:
            # print(_)  lable
            obj = [
                int((x1 + x2) / 2), int((y1 + y2) / 2),
                x2 - x1, y2 - y1
            ]
            bbox_xywh.append(obj)
            confs.append(conf)
            label.append(_)
        xywhs = torch.Tensor(bbox_xywh)
        confss = torch.Tensor(confs)

        # Pass detections to deepsort
        outputs = deepsort.update(xywhs, confss, image)

        # todo 摄像头捕获的数据
        # print("=================")

        # mask = 0
        # no_mask = 0
        # for i in range(len(outputs)):
        #     id_ = outputs[i][-1]
        #     try:
        #         label_ = label[i]
        #     except:
        #         label_ = "no_mask"

        #     # loop = asyncio.get_event_loop()
        #     # loop.run_until_complete(hello({
        #     #     "id": id_,
        #     #     "label": label_
        #     # }))

        #     if label_ == "mask":
        #         mask += 1
        #     else:
        #         no_mask += 1

        #     try:
        #         status_code = capture_requests_post({
        #             "id": id_,
        #             "label": label_
        #         })  # 数据上传服务器
        #         # print("picture upload state: ", status_code)
        #     except:
        #         print("无法连接到服务器")

        # 语音播报
        # if "no_mask" in label and time.time() - speak_old_time > 5:
        #     # os.system("mpg123 请佩戴口罩.mp3")
        #     song = AudioSegment.from_wav("请佩戴口罩.wav")
        #     play(song)
        #     speak_old_time = time.time()
        #     # try:
        #     #     _thread.start_new_thread(os.system, ("mpg123 请佩戴口罩.mp3",))
        #     # except:
        #     #     print("Error: 无法启动线程")

        # try:
        #     status_code = group_requests_post({
        #         "mask": mask,
        #         "no_mask": no_mask
        #     })  # 数据上传服务器
        #     # print("picture upload state: ", status_code)
        # except:
        #     print("无法连接到服务器")
        # print(post_data)
        # print("=================")

        for value in list(outputs):
            # print(value)
            x1, y1, x2, y2, track_id = value
            bboxes2draw.append(
                (x1, y1, x2, y2, "", track_id)
            )
    image = plot_bboxes(image, bboxes2draw)
    return image, bboxes2draw
