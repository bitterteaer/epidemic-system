from flask import g, Blueprint, redirect, url_for, request, jsonify, session, render_template, Response
from flask_login import login_required

from urls import yolo_api

bp = Blueprint("safety_hat", __name__, url_prefix="/safety_hat")


@bp.route("/index")
def index():
    session['real_time'] = request.args.get("real_time")
    content = {
        "admin": g.user,
        "video_feed_api": yolo_api,
        "real_time": session.get('real_time')
    }
    return render_template("safety_hat/index.html", **content)


@bp.route("/results_cut")
def results_cut():
    content = {
        "admin": g.user,
    }
    return render_template("safety_hat/results_cut.html", **content)


@bp.route("/camera_management")
def camera_management():
    content = {
        "admin": g.user,
        "max_display_page": 5,
        "page_size": 10
    }
    return render_template("safety_hat/camera_management.html", **content)


@bp.route("/camera_form")
def camera_form():
    content = {
        "admin": g.user,
    }
    return render_template("safety_hat/camera_form.html", **content)


@bp.route("/realtime")
def realtime():
    content = {
        "admin": g.user,
        "video_feed_api": yolo_api,
        "real_time": session.get('real_time')
    }
    return render_template("safety_hat/realtime.html", **content)


@bp.route("/data_statistics")
def data_statistics():
    content = {
        "admin": g.user
    }
    return render_template("safety_hat/data_statistics.html", **content)
