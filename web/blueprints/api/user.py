from flask import g, Blueprint, redirect, url_for, request, jsonify, session, render_template
from flask_login import login_user, logout_user

from common import Result
from exts import db
from models import User

from forms import LoginForm

bp = Blueprint("api_user", __name__, url_prefix="/api/user")


@bp.route("/login_in", methods=["POST"])
def login_in():
    lf = LoginForm(request.form)

    if not lf.validate():
        return Result.error(
            msg=str(lf.errors)
        )

    username = request.values.get("username")
    password = request.values.get("password")
    # print(username, password)

    user = db.session.query(User).filter(User.username == username).first()
    if user is None:
        return Result.error(
            msg="没有此用户"
        )
    else:
        if user.password == password:
            login_user(user)
            return Result.success(
                msg="登录成功"
            )
        else:
            return Result.error(
                msg="密码错误"
            )
