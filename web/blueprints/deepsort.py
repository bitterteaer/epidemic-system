from flask import g, Blueprint, redirect, url_for, request, jsonify, session, render_template, Response
from flask_login import login_required

from urls import deepsort_api

bp = Blueprint("deepsort", __name__, url_prefix="/deepsort")


@bp.route("/index")
def index():
    session['realtime'] = request.args.get("realtime")
    # print(request.args.get("realtime"))
    content = {
        "admin": g.user,
        "video_feed_api": deepsort_api,
        "realtime": session.get('realtime')
    }
    return render_template("deepsort/index.html", **content)


@bp.route("/results_cut")
def results_cut():
    content = {
        "admin": g.user,
        "video_feed_api": deepsort_api,
    }
    return render_template("deepsort/results_cut.html", **content)
