from variables import credentials_file, spreadsheet_id, scopes, tinkoff_api_token, sector
from oauth2client.service_account import ServiceAccountCredentials
from tinkoff_api import tinkoff_portfolio
from operator import itemgetter
from typing import NoReturn

import httplib2
import apiclient


# Отчистка таблицы от значений и стилей
def clear_sheet(sheets) -> NoReturn:
    sheets.spreadsheets().batchUpdate(
        spreadsheetId=spreadsheet_id,
        body={
            "requests": [
                # Удалить значение
                {
                    "updateCells": {
                        "range": {
                            "sheetId": 0
                        },
                        "fields": "userEnteredValue"
                    }
                },
                # Удалить стили
                {
                    "updateCells": {
                        "range": {
                            "sheetId": 0
                        },
                        "fields": "userEnteredFormat"
                    }
                },
                # Убрать объединение ячеек
                {
                    "unmergeCells": {
                        "range": {
                            "sheetId": 0
                        }
                    }
                }
            ]
        }
    ).execute()


# Добавить новое значение в таблицу
def add_data(counter_int: int, counter_str: str, values_1: str, values_2: float) -> dict:
    data_list = {
        "range": counter_str[0] + str(counter_int) + ':' + counter_str[1] + str(counter_int),
        "majorDimension": "ROWS",
        "values": [
            [
                values_1,
                values_2
            ]
        ]
    }

    return data_list


# Изменить стиль заднего фона (выделить жёлтым, если необходимо докупить актив)
def requests_background_color(counter: int) -> dict:
    request_list = {
        "repeatCell": {
            "range": {
                "sheetId": 0,
                "startRowIndex": counter - 1,
                "endRowIndex": counter,
                "startColumnIndex": 3,
                "endColumnIndex": 4
            },
            "cell": {
                "userEnteredFormat": {
                    "backgroundColor": {
                        "red": 1,
                        "green": 1,
                        "blue": 0
                    }
                }
            },
            "fields": "userEnteredFormat(backgroundColor)"
        }
    }

    return request_list


# Изменить формат на процент
def requests_percent(counter: int, column_index: int) -> dict:
    request_list = {
        "repeatCell": {
            "range": {
                "sheetId": 0,
                "startRowIndex": counter - 1,
                "endRowIndex": counter,
                "startColumnIndex": column_index,
                "endColumnIndex": column_index + 1
            },
            "cell": {
                "userEnteredFormat": {
                    # Изменить формат на процент
                    "numberFormat": {
                        "type": "PERCENT",
                        "pattern": '0.##%'
                    },
                    # Горизонтальное выравнивание
                    "horizontalAlignment": "CENTER",
                    # Вертикальное выравнивание
                    "verticalAlignment": "MIDDLE"
                }
            },
            "fields": "userEnteredFormat(numberFormat, horizontalAlignment, verticalAlignment)"
        }
    }

    return request_list


# Объединить ячейки
def request_merge_cells(end_row: int, start_row: int) -> dict:
    request_list = {
        "mergeCells": {
            "range": {
                "sheetId": 0,
                "startRowIndex": start_row - 1 if start_row != 0 else start_row,
                "endRowIndex": end_row - 1,
                "startColumnIndex": 0,
                "endColumnIndex": 2
            },
            "mergeType": "MERGE_COLUMNS"
        }
    }

    return request_list


# Формирование границ таблицы
def request_border(counter: int) -> dict:
    request_list = {
        "updateBorders": {
            "range": {
                "sheetId": 0,
                "startRowIndex": 0,
                "endRowIndex": counter - 1,
                "startColumnIndex": 0,
                "endColumnIndex": 4
            },
            "top": {
                "style": "SOLID",
                "width": 1
            },
            "bottom": {
                "style": "SOLID",
                "width": 1
            },
            "left": {
                "style": "SOLID",
                "width": 1
            },
            "right": {
                "style": "SOLID",
                "width": 1
            },
            "innerHorizontal": {
                "style": "SOLID",
                "width": 1
            },
            "innerVertical": {
                "style": "SOLID",
                "width": 1
            }
        }
    }

    return request_list


# Вертикальное выравнивание
def request_vertical_alignment(counter: int, column_index: int) -> dict:
    request_list = {
        "repeatCell": {
            "range": {
                "sheetId": 0,
                "startRowIndex": counter - 1,
                "endRowIndex": counter,
                "startColumnIndex": column_index,
                "endColumnIndex": column_index + 1
            },
            "cell": {
                "userEnteredFormat": {
                    "verticalAlignment": "MIDDLE"
                }
            },
            "fields": "userEnteredFormat(verticalAlignment)"
        }
    }

    return request_list


# Функция по заполнению google таблицы данными из tinkoff
def update_google_sheets() -> bool:
    # Массивы для заполнения и форматирования таблицы в Google Sheets
    data = []
    requests = []

    # Счётчики для заполнения и форматирования таблицы в Google Sheets
    counter_1 = 1
    counter_2 = 0

    # Авторизуемся и получаем service — экземпляр доступа к API
    credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials_file, scopes)
    http_auth = credentials.authorize(httplib2.Http())
    service = apiclient.discovery.build('sheets', 'v4', http=http_auth)

    # Очищаем таблицу
    clear_sheet(service)

    # Перебираем словарь сформированный Tinkoff Api
    for sector_string, assets_list in tinkoff_portfolio(tinkoff_api_token).items():
        # Добавляем значение сектора экономики и его процента
        data.append(add_data(counter_1, "AB", sector[sector_string], sum([assets_dict['percent'] for assets_dict in assets_list])))
        # Преобразуем формат процента сектора экономики из числа в процент
        requests.append(requests_percent(counter_1, 1))
        # Выравниваем вертикально значение сектора экономики и его процента
        requests.append(request_vertical_alignment(counter_1, 0))
        # Сортируем активы сектора экономики по уменьшению процента в портфеле
        assets_list.sort(key=itemgetter('percent'), reverse=True)
        # Перебираем массив из активов одного сектора экономики
        for assets_dict in assets_list:
            # Добавляем значение актива и его процента
            data.append(add_data(counter_1, "CD", assets_dict['name'], assets_dict['percent']))
            # Преобразуем формат процента актива из числа в процент
            requests.append(requests_percent(counter_1, 3))
            # Проверяем условие, что доля актива в портфеле менее 2,5%
            if assets_dict['percent'] <= 0.025:
                # Выделяем жёлтым цветом значение процента
                requests.append(requests_background_color(counter_1))
            # Увеличиваем счётчик для заполнения таблицы
            counter_1 += 1
        # Объединяем значение сектора экономики и его процента
        requests.append(request_merge_cells(counter_1, counter_2))
        # Увеличиваем счётчик для заполнения таблицы
        counter_2 = counter_1

    # Формирование границ таблицы
    requests.append(request_border(counter_2))

    # Формирования словаря для заполнения данными
    body_data = {
        "valueInputOption": "USER_ENTERED",
        "data": data,
    }

    # Формирование словаря для настройки стиля
    body_requests = {
        "requests": requests
    }

    # Заполнение таблицы данными
    service.spreadsheets().values().batchUpdate(spreadsheetId=spreadsheet_id, body=body_data).execute()
    # Заполнение таблицы стилями
    service.spreadsheets().batchUpdate(spreadsheetId=spreadsheet_id, body=body_requests).execute()

    return True
