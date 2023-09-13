from flask_sqlalchemy import SQLAlchemy
import time

db = SQLAlchemy()


def get_time():
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))


def dict_to_str(data):
    data = vars(data)
    for j in data.keys():
        data[j] = str(data[j])
    return data


def delete_sa_instance_state(data):
    data = vars(data)
    del data['_sa_instance_state']
    return data


if __name__ == "__main__":
    print(get_time())
