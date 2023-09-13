import _thread
import time

import requests
from flask import g, Blueprint, redirect, url_for, request, current_app, jsonify
from flask_login import login_user, logout_user

from exts import db, get_time, dict_to_str
from models import Capture, Mask


bp = Blueprint("api_mask", __name__, url_prefix="/api/mask")


send_mask_time = time.time()
send_number_time = time.time()


@bp.route("/group_set_data", methods=['POST'])
def group_set_data():
    global send_mask_time
    global send_number_time

    mask = int(request.form.get('mask'))
    no_mask = int(request.form.get('no_mask'))

    if no_mask > 0 and time.time()-send_mask_time > 10:
        send_mask_time = time.time()
        # 创建线程
        try:
            _thread.start_new_thread(requests.get, (f'http://127.0.0.1:5000/send_mail?title=口罩&data={no_mask}人没有佩戴口罩!', ))
        except Exception as e:
            print(e)
    if mask+no_mask >= 100 and time.time()-send_number_time > 10:
        send_number_time = time.time()
        # 创建线程
        try:
            _thread.start_new_thread(requests.get, (
            f'http://127.0.0.1:5000/send_mail?title=人流量&data=人员数量达到了{mask+no_mask}人!',))
        except Exception as e:
            print(e)

    group = Mask(
        mask=mask,
        no_mask=no_mask
    )
    db.session.add(group)
    db.session.commit()

    return jsonify({
        "mask": mask,
        "no_mask": no_mask
    })


@bp.route("/get_interactive_data")
def get_interactive_data():
    mask = []
    no_mask = []

    for i in db.session.query(Mask).order_by(Mask.id.desc()).paginate(page=1, per_page=40).items:
        mask.append(i.mask)
        no_mask.append(i.no_mask)

    data = {
        "series": [
            {
                'name': 'mask',
                'type': 'line',
                'stack': 'Total',
                'areaStyle': {},
                'emphasis': {
                    'focus': 'series'
                },
                'data': mask
            },
            {
                'name': 'no mask',
                'type': 'line',
                'stack': 'Total',
                'areaStyle': {},
                'emphasis': {
                    'focus': 'series'
                },
                'data': no_mask
            },
            {
                'name': 'all',
                'type': 'line',
                'stack': 'Total',
                'areaStyle': {},
                'emphasis': {
                    'focus': 'series'
                },
                'data': list(map(lambda x, y: x + y, mask, no_mask))
            },
        ]
    }

    return jsonify(data)


@bp.route("/get_zhuzhuangtu_data")
def get_zhuzhuangtu_data():
    group_all = db.session.query(Mask).all()
    count_mask = 0
    count_no_mask = 0
    for i in group_all:
        count_mask += int(i.mask)
        count_no_mask += int(i.no_mask)
    data = {
        "data": [
            {
                'value': count_mask,
                'itemStyle': {
                    'color': '#12ED93'
                }
            },
            {
                'value': count_no_mask,
                'itemStyle': {
                    'color': '#3F77FE'
                }
            },
            {
                'value': count_no_mask + count_mask,
                'itemStyle': {
                    'color': '#d223e7'
                }
            }
        ]
    }

    return jsonify(data)


@bp.route("/get_meiguitu_data")
def get_meiguitu_data():
    # count_mask = len(db.session.query(PassersBy).filter(PassersBy.person_label == "mask").all())
    # count_no_mask = len(db.session.query(PassersBy).filter(PassersBy.person_label == "no_mask").all())

    group_all = db.session.query(Mask).all()
    count_mask = 0
    count_no_mask = 0
    for i in group_all:
        count_mask += int(i.mask)
        count_no_mask += int(i.no_mask)

    # for i in db.session.query(GroupOfPeople).all():
    #     count_mask += int(i.mask)
    #     count_no_mask += int(i.no_mask)
    # mask = int(1000*count_mask/(count_mask+count_no_mask))
    data = {
        "data": [
            {'value': count_mask, 'name': 'mask'},
            {'value': count_no_mask, 'name': 'no mask'},
            {'value': count_mask + count_no_mask, 'name': 'all'}
        ]
    }

    return jsonify(data)
