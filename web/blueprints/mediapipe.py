from flask import g, Blueprint, redirect, url_for, request, jsonify, session, render_template, Response
from flask_login import login_required

from urls import mediapipe_api

bp = Blueprint("mediapipe", __name__, url_prefix="/mediapipe")


@bp.route("/index")
def index():
    session['realtime'] = request.args.get("realtime")
    # print(request.args.get("realtime"))
    content = {
        "admin": g.user,
        "video_feed_api": mediapipe_api,
        "realtime": session.get('realtime')
    }

    return render_template("mediapipe/index.html", **content)
