from flask import Flask
from datetime import timedelta
import os

from app.admin_staff import admin_staff_view
from app.auth import auth_view
from app.home import home_view
from app.user import user_view


def create_app():
    app = Flask(__name__)

    from app.weed import weed_view

    app.secret_key = "key"
    app.permanent_session_lifetime = timedelta(hours=24)
    UPLOAD_FOLDER = os.path.join(app.root_path, "static/images/db")
    app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

    app.register_blueprint(home_view.home_bp)
    app.register_blueprint(auth_view.auth_bp, url_prefix="/auth")
    app.register_blueprint(user_view.user_bp, url_prefix="/user")
    app.register_blueprint(admin_staff_view.admin_staff_bp, url_prefix="/admin_staff")
    app.register_blueprint(weed_view.weed_bp, url_prefix="/weed")

    return app
