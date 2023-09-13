from flask import g, Blueprint, redirect, url_for, request, jsonify, session, render_template, Response
from flask_login import login_required

from urls import yolo_api

bp = Blueprint("fire", __name__, url_prefix="/fire")


@bp.route("/index")
def index():
    session['realtime'] = request.args.get("realtime")
    content = {
        "admin": g.user,
        "video_feed_api": yolo_api,
        "realtime": session.get('realtime')
    }
    return render_template("fire/index.html", **content)
