from flask import Blueprint, render_template, send_from_directory
from parslib.services.librus_api import intrllibrus
from .plan_zajec import bp as teacher_schedule_bp
import os

bp = Blueprint('main', __name__)
bp.register_blueprint(teacher_schedule_bp)
@bp.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(bp.root_path, '..', 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@bp.route('/home')
def home():
    interfejs, username, user_log = intrllibrus()
    return render_template('index.html', interfejs=interfejs, username=username, user_log=user_log)