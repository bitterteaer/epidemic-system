from flask import g, Flask, render_template, session, redirect, request
from flask_login import LoginManager, current_user
from flask_migrate import Migrate

import configs
from exts import db
from models import User
from blueprints.user import bp as user_bp
from blueprints.mask import bp as mask_bp
from blueprints.safety_hat import bp as safety_hat_bp
from blueprints.unet import bp as unet_bp
from blueprints.deepsort import bp as deepsort_bp
from blueprints.mediapipe import bp as mediapipe_bp
from blueprints.fire import bp as fire_bp
from blueprints.api.passers_by import bp as passers_by_bp
from blueprints.api.user import bp as api_user_bp
from blueprints.api.fire import bp as api_fire_bp
from blueprints.api.mask import bp as api_mask_bp
from blueprints.api.safety_hat import bp as api_safety_hat_bp
from blueprints.api.capture import bp as api_capture_bp


app = Flask(__name__)

# app.app_context().push()
app.config.from_object(configs)
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "visitor.main"
login_manager.login_message_category = "warning"

app.register_blueprint(user_bp)
app.register_blueprint(mask_bp)
app.register_blueprint(safety_hat_bp)
app.register_blueprint(api_user_bp)
app.register_blueprint(api_mask_bp)
app.register_blueprint(api_capture_bp)
app.register_blueprint(api_safety_hat_bp)
app.register_blueprint(unet_bp)
app.register_blueprint(passers_by_bp)
app.register_blueprint(deepsort_bp)
app.register_blueprint(mediapipe_bp)
app.register_blueprint(fire_bp)
app.register_blueprint(api_fire_bp)

migrate = Migrate(app, db)


@login_manager.user_loader
def load_user(user_id):
    user = User.query.get(int(user_id))
    return user


@app.before_request
def before_request():
    # g.my_redis = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
    if current_user.is_authenticated:
        g.user = current_user


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        debug=True
    )
