from exts import get_time
from flask import jsonify


class Result(object):
    @staticmethod
    def success(code=0, msg="success", data=None, count=0):
        return jsonify({
            "code": code,
            "msg": msg,
            "data": data,
            "count": count,
            "time": get_time(),
            'success': True
        })

    @staticmethod
    def error(code=1, msg="error", data=None, count=0):
        return jsonify({
            "code": code,
            "msg": msg,
            "data": data,
            "count": count,
            "time": get_time(),
            'success': False
        })
