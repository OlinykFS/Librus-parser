from flask import Blueprint, render_template, jsonify
from parslib.services.librus_api import intrllistaklas, intrlistauczniow, intruczen_data, ocfr_niedostateczne

bp = Blueprint('students', __name__)

@bp.route('/klasy', methods=['GET'])
def klasy():
    url = "https://synergia.librus.pl/przegladaj_oceny"
    klasy = intrllistaklas(url)
    return render_template('klasy.html', klasy=klasy)

@bp.route('/lista_uczniow/<class_id>', methods=['GET', 'POST'])
def lista_uczniow(class_id):
    url = f'https://synergia.librus.pl/przegladaj_oceny/wguczniow/{class_id}'
    uczniowie = intrlistauczniow(url)
    return render_template('lista_uczniow.html', uczniowie=uczniowie)

@bp.route('/uczen_data/<int:student_id>', methods=['GET', 'POST'])
def uczen_data(student_id):
    url = f'https://synergia.librus.pl/przegladaj_oceny/uczen/{student_id}'
    oceny_dict = intruczen_data(url)
    uczen_info = intrlistauczniow(url)
    return render_template('uczen_data.html', oceny_dict=oceny_dict, uczen_info=uczen_info)

@bp.route('/ocfr_niedostateczne')
def ocfr_niedostateczne_route():
    results = ocfr_niedostateczne()
    grouped_results = {}
    for student in results:
        class_name = student['number'].split()[0]
        if class_name not in grouped_results:
            grouped_results[class_name] = []
        grouped_results[class_name].append(student)
    return render_template('ocfrNdst.html', grouped_results=grouped_results)