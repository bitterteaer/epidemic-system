from flask import g, Blueprint, redirect, url_for, request, jsonify, session, render_template
from flask_login import login_user, logout_user

from common import Result
from exts import db
from models import PassersBy, Fire

bp = Blueprint("api_fire", __name__, url_prefix="/api/fire")


@bp.route("/set_data", methods=["POST"])
def set_data():
    fire_warn = request.form.get("fire_warn")
    print(fire_warn)

    f = Fire(
        fire_warn=fire_warn
    )

    db.session.add(f)
    db.session.commit()

    return "success"
