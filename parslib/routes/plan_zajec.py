from flask import Blueprint, render_template
from parslib.services.librus_api import schedule


bp = Blueprint('teacher_schedule', __name__)


@bp.route('/teacher_schedule')
def teacher_schedule():
    url = f'https://synergia.librus.pl/plan_lekcji'
    plan_zajec = schedule(url)
    return render_template('plan-zajec.html', plan_zajec=plan_zajec)

