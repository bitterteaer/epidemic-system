from flask import g, Blueprint, redirect, url_for, request, jsonify, session, render_template
from flask_login import login_user, logout_user, login_required

bp = Blueprint("user", __name__, url_prefix="/")


@bp.route("/")
def main():
    return render_template("login.html")


@bp.route("/index")
@login_required
def index():
    content = {
        "admin": g.user,
    }
    return render_template("index.html", **content)


@bp.route("/login_out", methods=['GET'])
def login_out():
    """删除session数据"""
    if session.get("id_user"):
        del session["id_user"]

    logout_user()
    return "success"
