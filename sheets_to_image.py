import requests
import fitz
import os


# Преобразуем Google sheets в png
def creating_pictures(spreadsheet_id: str) -> list:
    # Массив названий картинок
    image_list = []

    # Ссылка на скачивания таблицы из Google sheets
    url = f'https://docs.google.com/spreadsheets/d/{spreadsheet_id}/export?format=pdf&gid=0'

    # Скачивание pdf файла с google sheets
    response = requests.get(url)

    # Сохранение файла pdf
    with open("portfolio_diversification.pdf", "wb") as pdf_file:
        pdf_file.write(response.content)

    # Преобразование pdf в png
    for page in fitz.open("portfolio_diversification.pdf"):
        page.get_pixmap().save(f"portfolio_diversification{page.number}.png")
        image_list.append(f"portfolio_diversification{page.number}.png")

    return image_list


# Удаление файлов pdf и png
def del_file(path_list: list) -> None:
    # Перебираем массив файлов, если файл есть, то удаляем
    for path in path_list:
        if os.path.isfile(path):
            os.remove(path)
