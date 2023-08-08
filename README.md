# Диверсификация портфеля

## Суть проекта
Формирование таблицы "Диверсификация портфеля" и отправка её с использованием бота Телеграм.
Для формирования таблицы необходимо проанализировать активы (акции, облигации) брокерского портфеля Тинькофф.
В портфеле формируется таблица по секторам экономики и активам. Если актив в портфеле занимает менее 2,5% - таблица выделяется жёлтым цветом, что обозначает необходимость усреднить данный актив.

## Стек
- [Tinkoff Invest](https://github.com/Tinkoff/invest-python)
- [API Google Workspace](https://developers.google.com/sheets/api/quickstart/python?hl=ru)
- [PyMuPDF](https://pymupdf.readthedocs.io/en/latest/index.html)
- [Aiogram](https://docs.aiogram.dev/en/latest/)

## Начало работы
<!-- termynal -->
```
pip install tinkoff-investments
```
```
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib oauth2client
```
```
pip install --upgrade pymupdf
```
```
pip install -U aiogram
```

# Как пользоваться
В файле variables.py необходимо указать свои переменные.

- tinkoff_api_token - токен для Тинькофф инвестиций, получить можно по следующей [инструкции](https://tinkoff.github.io/investAPI/token/#:~:text=%D1%80%D0%B0%D0%B1%D0%BE%D1%82%D0%BE%D1%81%D0%BF%D0%BE%D1%81%D0%BE%D0%B1%D0%BD%D0%BE%D1%81%D1%82%D0%B8%20%D0%B2%D1%81%D0%B5%D1%85%20%D0%B0%D0%BB%D0%B3%D0%BE%D1%80%D0%B8%D1%82%D0%BC%D0%BE%D0%B2.-,%D0%9F%D0%BE%D0%BB%D1%83%D1%87%D0%B5%D0%BD%D0%B8%D0%B5%20%D1%82%D0%BE%D0%BA%D0%B5%D0%BD%D0%B0,-%D0%9F%D0%B5%D1%80%D0%B5%D0%B9%D0%B4%D0%B8%D1%82%D0%B5%20%D0%B2%20%D0%BD%D0%B0%D1%81%D1%82%D1%80%D0%BE%D0%B9%D0%BA%D0%B8).
- aiogram_api_token - токен для Телеграм, получить можно по следующей [инструкции](https://botcreators.ru/blog/botfather-instrukciya/).
- telegram_my_id - Ваш id в Телеграм, получить можно по следующей [инструкции](https://perfluence.net/blog/article/kak-uznat-id-telegram#:~:text=%D0%9A%D0%B0%D0%BA%20%D0%A3%D0%B7%D0%BD%D0%B0%D1%82%D1%8C%20%D0%A1%D0%B2%D0%BE%D0%B9%20ID%20Telegram%3F).
- credentials_file - токен для Google, получить можно по следующей [инструкции](https://www.youtube.com/watch?v=Bf8KHZtcxnA).
- spreadsheet_id - id Вашей Google таблицы, получить можно по следующей [инструкции](https://www.oksheets.com/get-spreadsheet-id/#:~:text=%D0%9D%D0%B0%D0%B9%D0%B4%D0%B8%D1%82%D0%B5%20%D0%B8%D0%B4%D0%B5%D0%BD%D1%82%D0%B8%D1%84%D0%B8%D0%BA%D0%B0%D1%82%D0%BE%D1%80%20%D1%8D%D0%BB%D0%B5%D0%BA%D1%82%D1%80%D0%BE%D0%BD%D0%BD%D0%BE%D0%B9%20%D1%82%D0%B0%D0%B1%D0%BB%D0%B8%D1%86%D1%8B%20Google%2C%20%D0%B8%D1%81%D0%BF%D0%BE%D0%BB%D1%8C%D0%B7%D1%83%D1%8F%20URL%2D%D0%B0%D0%B4%D1%80%D0%B5%D1%81).

# Результат
Таким образом получаем следующий функционал в Телеграм боте
<div style="display: flex">
<img src="/img/1.jpg" width="300">
<img src="/img/2.jpg" width="300">
</div>
