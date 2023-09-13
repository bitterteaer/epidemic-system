import os
import time
# import redis
from flask import g, Blueprint, redirect, url_for, request, current_app, jsonify
from flask_login import login_user, logout_user

from exts import db, get_time, dict_to_str
from models import Capture, Mask


bp = Blueprint("api_capture", __name__, url_prefix="/api/capture")


@bp.route("/save_picture_cut", methods=['POST'])
def save_picture_cut():
    pic_type = request.form.get("pic_type")
    uploaded_file = request.files.get('file')

    suffix = '.' + uploaded_file.filename.split('.')[-1]  # 获取文件后缀名
    filename = uploaded_file.filename.replace(".", "").replace("\\", "").replace("/", "")
    # basedir = os.path.abspath(os.path.dirname(__file__)).replace("blueprints", "")  # 获取当前文件路径
    filename = filename + str(time.time()).replace(".", "") + suffix  # 拼接相对路径
    new_dir = os.path.join("static", "save_picture_cut", filename)
    uploaded_file_path = os.path.join(current_app.root_path, new_dir)  # 拼接图片完整保存路径,时间戳命名文件防止重复

    uploaded_file.save(uploaded_file_path)  # 保存文件
    # r = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, password=PASS_WORD)
    # r.set("realtime_frame", new_dir)
    print("new_dir:", new_dir)
    # size = os.path.getsize(uploaded_file_path)

    pc = Capture(
        path="/"+new_dir.replace("\\", "/"),
        pic_type=pic_type
    )

    db.session.add(pc)
    db.session.commit()

    return "success"


@bp.route("/get_picture_cut", methods=["GET"])
def get_picture_cut():
    page = request.args.get("limit")
    size = request.args.get('size')
    pic_type = request.args.get('pic_type')
    # print(page, size, pic_type)
    total = len(db.session.query(Capture).filter(Capture.pic_type == pic_type).all())
    try:
        # video_list = db.session.query(Capture).filter(Capture.pic_type == pic_type).order_by(Capture.id.desc()).paginate(page=int(1), per_page=int(12)).items
        video_list = db.session.query(Capture).filter(Capture.pic_type == pic_type).order_by(Capture.id.desc()).paginate(page=int(page), per_page=int(size)).items
        # print("video_list:", video_list)
    except Exception as e:
        print(e)
        return "error"

    return jsonify({
        'tableData': list(map(dict_to_str, video_list)),
        'total': total
    })
