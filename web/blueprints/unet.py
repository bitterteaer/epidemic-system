from flask import g, Blueprint, redirect, url_for, request, jsonify, session, render_template, Response
from flask_login import login_required

from urls import unet_api

bp = Blueprint("unet", __name__, url_prefix="/unet")


@bp.route("/index")
def index():
    content = {
        "admin": g.user,
        "unet_api": unet_api,
    }
    return render_template("unet/index.html", **content)


@bp.route("/random_sample_display")
def random_sample_display():
    content = {
        "admin": g.user,
        "unet_api": unet_api,
    }
    return render_template("unet/random_sample_display.html", **content)


@bp.route("/upload_split")
def upload_split():
    content = {
        "admin": g.user,
        "unet_api": unet_api,
    }
    return render_template("unet/upload_split.html", **content)
