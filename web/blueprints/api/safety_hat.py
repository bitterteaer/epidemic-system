import os
import time
import redis
from flask import g, Blueprint, redirect, url_for, request, current_app, jsonify
from flask_login import login_user, logout_user

from exts import db, get_time, dict_to_str
from models import Capture, Mask, SafetyHat

bp = Blueprint("api_safety_hat", __name__, url_prefix="/api/safety_hat")


@bp.route("/group_set_data", methods=['POST'])
def group_set_data():
    safety_hat = int(request.form.get('safety_hat'))
    no_safety_hat = int(request.form.get('no_safety_hat'))

    group = SafetyHat(
        safety_hat=safety_hat,
        no_safety_hat=no_safety_hat
    )
    db.session.add(group)
    db.session.commit()

    return "success"


@bp.route("/get_interactive_data")
def get_interactive_data():
    safety_hat = []
    no_safety_hat = []

    for i in db.session.query(SafetyHat).order_by(SafetyHat.id.desc()).paginate(page=1, per_page=40).items:
        safety_hat.append(i.safety_hat)
        no_safety_hat.append(i.no_safety_hat)

    data = {
        "series": [
            {
                'name': 'safety_hat',
                'type': 'line',
                'stack': 'Total',
                'areaStyle': {},
                'emphasis': {
                    'focus': 'series'
                },
                'data': safety_hat
            },
            {
                'name': 'no safety_hat',
                'type': 'line',
                'stack': 'Total',
                'areaStyle': {},
                'emphasis': {
                    'focus': 'series'
                },
                'data': no_safety_hat
            },
            {
                'name': 'all',
                'type': 'line',
                'stack': 'Total',
                'areaStyle': {},
                'emphasis': {
                    'focus': 'series'
                },
                'data': list(map(lambda x, y: x + y, safety_hat, no_safety_hat))
            },
        ]
    }

    return jsonify(data)


@bp.route("/get_zhuzhuangtu_data")
def get_zhuzhuangtu_data():
    group_all = db.session.query(SafetyHat).all()
    count_safety_hat = 0
    count_no_safety_hat = 0
    for i in group_all:
        count_safety_hat += int(i.safety_hat)
        count_no_safety_hat += int(i.no_safety_hat)
    data = {
        "data": [
            {
                'value': count_safety_hat,
                'itemStyle': {
                    'color': '#12ED93'
                }
            },
            {
                'value': count_no_safety_hat,
                'itemStyle': {
                    'color': '#3F77FE'
                }
            },
            {
                'value': count_safety_hat + count_no_safety_hat,
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

    group_all = db.session.query(SafetyHat).all()
    count_safety_hat = 0
    count_no_safety_hat = 0
    for i in group_all:
        count_safety_hat += int(i.safety_hat)
        count_no_safety_hat += int(i.no_safety_hat)

    # for i in db.session.query(GroupOfPeople).all():
    #     count_mask += int(i.mask)
    #     count_no_mask += int(i.no_mask)
    # mask = int(1000*count_mask/(count_mask+count_no_mask))
    data = {
        "data": [
            {'value': count_safety_hat, 'name': 'safety_hat'},
            {'value': count_no_safety_hat, 'name': 'no safety_hat'},
            {'value': count_safety_hat + count_no_safety_hat, 'name': 'all'}
        ]
    }

    return jsonify(data)
