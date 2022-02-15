import gspread
from oauth2client.service_account import ServiceAccountCredentials
from config import URL_1, URL_2, URL_3

# технические данные - подключение к Google Sheets API
scope = ["https://spreadsheets.google.com/feeds",
         'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file",
         "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("files/credentials.json", scope)
client = gspread.authorize(creds)

# названия столбцов
columns = ['Название команды', 'Количество участников', 'Участники',
           'Номер капитана', 'Почта капитана', 'Учебное заведение', 'Пароль']


def save_data(data):  # функция сохранения данных в гугл-таблицу
    # подключаемся к первому доступному листу
    worksheet = client.open_by_url(URL_1).sheet1
    request_data = worksheet.get_all_records()
    # проверяем, введены ли уже названия столбцов, если нет - добавляем
    if not request_data:
        cell_list = worksheet.range('A1:G1')
        for i in range(len(cell_list)):
            cell_list[i].value = columns[i]
        worksheet.update_cells(cell_list)

    # получаем данные об уже заполненных строках и добавляем данные на следующую свободную
    cell_list = worksheet.range(f'A{len(request_data) + 2}:G{len(request_data) + 2}')
    for i in range(len(cell_list)):
        if isinstance(data[i], list):
            dt = ', '.join(data[i])
            cell_list[i].value = dt
        else:
            cell_list[i].value = data[i]
    worksheet.update_cells(cell_list)


def get_info():
    worksheet = client.open_by_url(URL_2).sheet1
    request_data = worksheet.get_all_values()
    values = []
    for value in request_data:
        values.append(value[1])
    return values[0], values[1], values[2]


def get_questions():
    worksheet = client.open_by_url(URL_3).sheet1
    request_data = worksheet.get_all_values()
    values = {}
    for value in request_data:
        question = value[0]
        value.pop(0)
        values[question] = value

    return values, len(request_data)


