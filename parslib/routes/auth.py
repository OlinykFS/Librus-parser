from flask import Blueprint, render_template, request, redirect, url_for,jsonify
from parslib.services.librus_api import login, logout as librus_logout
from parslib.services.data_service import save_credentials

bp = Blueprint('auth', __name__)

@bp.route('/', methods=['GET', 'POST'])
def authentication():
    if request.method == 'POST':
        username = request.form.get('login')
        password = request.form.get('pass')
        save_credentials(username, password)
        if login():
            return redirect(url_for('main.home'))
        else:
            error = 'Invalid login or password'
            return render_template('login.html', error=error)
    return render_template('login.html')


@bp.route('/logout', methods=['POST', 'GET'])
def logout():
    librus_logout()
    return redirect(url_for('auth.authentication'))