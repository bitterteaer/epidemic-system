from flask import g, Blueprint, redirect, url_for, request, jsonify, session, render_template, Response
from flask_login import login_required

from urls import all_urls
import requests

bp = Blueprint("manager", __name__, url_prefix="/manager")


@bp.before_request
@login_required
def before_request():
    pass


@bp.route("/index")
def index():
    for i_index, i in enumerate(all_urls):
        try:
            ret = requests.get(i["url"], timeout=0.1)
            all_urls[i_index]["state"] = "open"
        except Exception as e:
            print(e)
            all_urls[i_index]["state"] = "close"

    content = {
        "admin": g.user,
        "all_urls": all_urls
    }
    return render_template("manager/index.html", **content)
