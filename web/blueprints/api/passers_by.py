from flask import g, Blueprint, redirect, url_for, request, jsonify, session, render_template
from flask_login import login_user, logout_user

from common import Result
from exts import db
from models import PassersBy

bp = Blueprint("api_passers_by", __name__, url_prefix="/api/passers_by")


@bp.route("/get_data")
def get_data():
    return db.session.query(PassersBy).all()


@bp.route("/set_data", methods=["POST"])
def set_data():
    down_count = request.form.get("down_count")
    up_count = request.form.get("up_count")

    pb = PassersBy(
        down_count=down_count,
        up_count=up_count
    )

    db.session.add(pb)
    db.session.commit()

    return "success"


@bp.route("/get_interactive_data")
def get_interactive_data():
    up_count = []
    down_count = []

    for i in db.session.query(PassersBy).order_by(PassersBy.id.desc()).paginate(page=1, per_page=40).items:
        up_count.append(i.up_count)
        down_count.append(i.down_count)

    data = {
        "series": [
            {
                'name': 'up',
                'type': 'line',
                'stack': 'Total',
                'areaStyle': {},
                'emphasis': {
                    'focus': 'series'
                },
                'data': up_count
            },
            {
                'name': 'down',
                'type': 'line',
                'stack': 'Total',
                'areaStyle': {},
                'emphasis': {
                    'focus': 'series'
                },
                'data': down_count
            },
            {
                'name': 'all',
                'type': 'line',
                'stack': 'Total',
                'areaStyle': {},
                'emphasis': {
                    'focus': 'series'
                },
                'data': list(map(lambda x, y: x + y, up_count, down_count))
            },
        ]
    }

    return jsonify(data)


@bp.route("/get_zhuzhuangtu_data")
def get_zhuzhuangtu_data():
    # group_all = db.session.query(PassBy).all()
    # up_count = 0
    # down_count = 0
    pb = db.session.query(PassersBy).order_by(PassersBy.id.desc()).first()
    # for i in group_all:
    #     count_mask += int(i.mask)
    #     count_no_mask += int(i.no_mask)
    data = {
        "data": [
            {
                'value': pb.up_count,
                'itemStyle': {
                    'color': '#12ED93'
                }
            },
            {
                'value': pb.down_count,
                'itemStyle': {
                    'color': '#3F77FE'
                }
            },
            {
                'value': pb.up_count + pb.down_count,
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

    pb = db.session.query(PassersBy).order_by(PassersBy.id.desc()).first()
    # count_mask = 0
    # count_no_mask = 0
    # for i in group_all:
    #     count_mask += int(i.mask)
    #     count_no_mask += int(i.no_mask)

    # for i in db.session.query(GroupOfPeople).all():
    #     count_mask += int(i.mask)
    #     count_no_mask += int(i.no_mask)
    # mask = int(1000*count_mask/(count_mask+count_no_mask))
    data = {
        "data": [
            {'value': pb.up_count, 'name': 'up'},
            {'value': pb.down_count, 'name': 'down'},
            {'value': pb.up_count + pb.down_count, 'name': 'all'}
        ]
    }

    return jsonify(data)
