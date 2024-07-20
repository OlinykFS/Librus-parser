import re
import bs4
import requests
import time
import fake_useragent
from urllib3.util import url

from parslib.services.data_service import get_credentials

LINK_AUTH = "https://api.librus.pl/OAuth/Authorization?client_id=47"
USER_AGENT = fake_useragent.UserAgent().random
HEADERS = {'user-agent': USER_AGENT}

session = requests.Session()


def login():
    credentials = get_credentials()
    preconnect = session.get('https://api.librus.pl/OAuth/Authorization?client_id=47&response_type=code&scope=mydata')
    response = session.post(LINK_AUTH, data=credentials, headers=HEADERS)
    if response.status_code == 200:
        succesconn = session.get('https://api.librus.pl/OAuth/Authorization/2FA?client_id=47')
        return succesconn
def logout():
    global session
    session.get('https://synergia.librus.pl/wyloguj')
    session = requests.Session()

def intrllibrus():
    intrlession = session.get('https://synergia.librus.pl/interfejs_lekcyjny')
    soup = bs4.BeautifulSoup(intrlession.text, 'lxml')
    user_section = soup.find("div", id='user-section')

    user_log = ""
    username = ""
    if user_section:
        log_tag = user_section.find("span", class_='tooltip')
        name_tag = user_section.find("b")
        if name_tag:
            user_log = log_tag.text.strip()
            username = name_tag.text.strip()
    return intrlession.text, username, user_log


def intrllistaklas(url):
    response = session.get(url)
    soup = bs4.BeautifulSoup(response.text, 'lxml')
    klasy_set = set()
    for tr in soup.find_all('tr'):
        name_th = tr.find('th', class_='big')
        script_td = tr.find('td', class_='left')
        if name_th and script_td:
            name = name_th.text.strip()
            script = script_td.find('script', type='text/javascript')
            if script:
                script_content = script.string
                match = re.search(r'window\.location\.href\s*=\s*"\\/przegladaj_oceny\\/wguczniow\\/(\d+)"',
                                  script_content)
                if match:
                    id = match.group(1)
                    klasy_set.add((name, id))
    return [{'klas': klas[0], 'id': klas[1]} for klas in sorted(klasy_set)]



def intrlistauczniow(url):
    response = session.get(url)
    soup = bs4.BeautifulSoup(response.text, 'lxml')
    uczniowie = []
    for i, tr in enumerate(soup.find_all('tr'), start=-1):
        name_td = tr.find('td', class_='')
        script_td = tr.find('td', class_='small')
        if name_td and script_td:
            name = name_td.text.strip()
            script = script_td.find('script', type='text/javascript')
            if script:
                script_content = script.string
                match = re.search(r'window\.location\.href\s*=\s*"\\/przegladaj_oceny\\/uczen\\/(\d+)"', script_content)

                if match:
                    student_id = match.group(1)
                    uczniowie.append({'name': name, 'id': student_id, 'number': i})
    return uczniowie



def ocfr_niedostateczne():
    url = "https://synergia.librus.pl/statystyki"
    headers = {
        "Host": "synergia.librus.pl",
        "Cookie": "; ".join([f"{k}={v}" for k, v in session.cookies.get_dict().items()]),
        "User-Agent": USER_AGENT,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    def fetch_data(ukryj_uczniow_nkl):
        payload = {
            "nazwaStatystyki": "Uczniowie z oceną niedostateczną",
            "rodzajStatystyki": "12",
            "rodzaj_ocen": "3",
            "ukryj_uczniow_nkl": str(ukryj_uczniow_nkl),
            "filtruj_id_jednostki": "-1",
            "filtruj_id_klasy": "-1",
            "poziom_od": "",
            "poziom_do": "",
            "filtruj": "Filtruj",
            "reczny_submit": "1",
            "numer_strony": "0"
        }
        students = []
        page = 0
        while True:
            payload["numer_strony"] = str(page)
            try:
                response = session.post(url, data=payload, headers=headers)
                response.raise_for_status()
            except requests.exceptions.RequestException as e:
                print(f"aye(: {e}")
                break
            soup = bs4.BeautifulSoup(response.text, 'lxml')
            table = soup.find('table', class_='decorated large center statisticTable')

            if table:
                rows = table.find('tbody').find_all('tr')
                for row in rows:
                    cols = row.find_all('td')
                    if len(cols) >= 4:
                        students.append({
                            'number': cols[0].text.strip(),
                            'name': cols[2].text.strip(),
                            'subject': cols[4].text.strip(),
                            'student_id': cols[1].text.strip(),
                            'status': 'NK' if ukryj_uczniow_nkl == 0 else 'Promoted'
                        })

                next_page = soup.find('a', text=re.compile('Następna'))
                if next_page:
                    page += 1
                    time.sleep(1)
                else:
                    break
            else:
                break

        return students

    all_students = fetch_data(0)
    promoted_students = fetch_data(1)

    promoted_dict = {(s['number'], s['name'], s['subject']): s for s in promoted_students}

    for student in all_students:
        key = (student['number'], student['name'], student['subject'])
        if key in promoted_dict:
            student['status'] = 'Promoted'

    return all_students


def intruczen_data(url):
    response = session.get(url)
    soup = bs4.BeautifulSoup(response.text, 'lxml')
    oceny_dict = {}
    przedmioty_info = soup.select('tr.line0, tr.line1')
    for tr in przedmioty_info:
        przedmiot_td = tr.find('td', class_='center micro screen-only')

        if przedmiot_td:
            przedmiot = przedmiot_td.find_next_sibling('td')
            if przedmiot and not przedmiot.has_attr('class'):
                subject_name = przedmiot.text.strip()

                if subject_name not in oceny_dict:
                    oceny_dict[subject_name] = []

                oceny = tr.find_all('a', class_='ocena')

                if oceny:
                    for ocena in oceny:
                        oceny_dict[subject_name].append(ocena.text.strip())

    return oceny_dict


def schedule(url):
    response = session.get(url)
    soup = bs4.BeautifulSoup(response.text, 'lxml')

    table = soup.find('table', class_='decorated plan-lekcji')

    timetable = []

    if table:
        headers = []
        thead = table.find('thead')

        if thead:
            for header in thead.find_all('td'):
                headers.append(header.get_text(separator=" ").strip())
            timetable.append(headers)
        else:
            print("thead ne aye")

        for row in table.find_all('tr'):
            if 'line1' in row.get('class', []):
                cols = row.find_all(['td', 'th'])
                data_row = []
                for col in cols:

                    text = col.get_text(separator=" ").strip().replace('\xa0', ' ')
                    if text == "":
                        text = None
                    data_row.append(text)
                timetable.append(data_row)

    else:
        print("table ne aye")
    return timetable
