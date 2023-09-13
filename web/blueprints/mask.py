from flask import g, Blueprint, redirect, url_for, request, jsonify, session, render_template, Response
from flask_login import login_required

from urls import yolo_api

bp = Blueprint("mask", __name__, url_prefix="/mask")


@bp.route("/index")
def index():
    session['real_time'] = request.args.get("real_time")
    content = {
        "admin": g.user,
        "video_feed_api": yolo_api,
        "real_time": session.get('real_time')
    }
    return render_template("mask/index.html", **content)


@bp.route("/results_cut")
def results_cut():
    pic_type = request.args.get("pic_type")
    content = {
        "admin": g.user,
        "pic_type": pic_type
    }
    return render_template("mask/results_cut.html", **content)


@bp.route("/camera_form")
def camera_form():
    content = {
        "admin": g.user,
    }
    return render_template("mask/camera_form.html", **content)


@bp.route("/realtime")
def realtime():
    content = {
        "admin": g.user,
        "video_feed_api": yolo_api,
        "real_time": session.get('real_time')
    }
    return render_template("mask/realtime.html", **content)


@bp.route("/data_statistics")
def data_statistics():
    content = {
        "admin": g.user
    }
    return render_template("mask/data_statistics.html", **content)
