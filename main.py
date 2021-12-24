import datetime
from datetime import date
import gspread
from oauth2client.service_account import ServiceAccountCredentials  # Ипортируем ServiceAccountCredentials
import pprint  # импортируем pprint
import time
from redis import Redis
from rq import Queue
import schedule

q = Queue(connection=Redis())

link = ['https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive']  # Задаем ссылку на Гугл таблици
my_creds = ServiceAccountCredentials.from_json_keyfile_name('goluboe.json',
                                                            link)  # Формируем данные для входа из нашего json файла

client = gspread.authorize(my_creds)  # Запускаем клиент для связи с таблицами
sheet = client.open('Goluboe').sheet1  # Открываем нужную на таблицу и лист
printf = pprint.PrettyPrinter()  # Описываем прити принт

get_data = sheet.get_all_records()  # Получаем все данные из таблици
get_data1 = sheet.row_values(2)
get_data2 = sheet.col_values(2)
get_data3 = sheet.cell(2, 2).value


def exel_cleaner():
    for n in range(2):
        x = n
        a = date.today() + datetime.timedelta(days=n)
        sheet.update_cell(1, x + 2, str(a))
    for n in range(2, 10):
        sheet.update_cell(n, 2, '')
        sheet.update_cell(n, 2, sheet.cell(n, 3).value)
        sheet.update_cell(n, 3, '')


schedule.every().day.at("21:00").do(exel_cleaner)



while True:
    schedule.run_pending()
    time.sleep(1)

