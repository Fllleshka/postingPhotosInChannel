from datetime import datetime, timedelta
import datetime
import os
import random
import time
import sqlite3
import telebot
from database.botdates import *

# Инициируем таблицу для хранения записей о картинках вида:
# id | name_pic | timetopost
# айди строки | Название фотографии в папке | Время её постинга
def initialdatabase():
    # Открываем соединение с базой данных
    con = sqlite3.connect(pathdb)
    # Создаём таблицу постинга
    with con:
        con.execute(
            """
                CREATE TABLE IMAGES (
                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    name_pic TEXT,
                    timetopost datetime
                );
            """
        )
    # Закрываем соединение с базой данных
    con.close()

# Заполняем таблицу данными о названиях картинок и времени постинга
def importphotos():
    # Открываем соединение с базой данных
    con = sqlite3.connect(pathdb)
    # Данные для базы данных
    sql = 'INSERT INTO IMAGES (id, name_pic, timetopost) values(?,?,?)'
    dates = []

    # Импортируем картинки из папок
    files = os.listdir("database/photos/")
    print(files)
    files.sort()
    # Создаём переменные для показывания процентов
    i = 0
    # Пробегаемся по элементам в списке
    timetopost = datetime.datetime.today()
    for element in files:
        i += 1
        persentstep = round(100 * float(i) / float(len(files)), 2)
        time2 = datetime.timedelta(minutes = random.randint(10, 20), seconds = random.randint(1, 60))
        timetopost += time2
        dates.append((i, element, timetopost.strftime("%Y-%m-%d %H:%M:%S")))
    with con:
        con.executemany(sql, dates)
    con.close()

# Функция импорта данных для постинга на день
def datesfromtable():
    # Соединение с базой данных
    con = sqlite3.connect(pathdb)
    today = datetime.datetime.today()
    todayday = today.strftime("%Y-%m-%d")
    starttime = todayday + " 00:00:01"
    endtime = todayday + " 23:59:59"
    query = "SELECT * FROM IMAGES WHERE timetopost >= '" + starttime + "' and timetopost <= '" + endtime + "'"
    with con:
        data = con.execute(query).fetchall()
    con.close()
    return data

# Класс времена, используется для запуска событий по определённому времени
class times:
    printPhoto = (datetime.datetime.today() + timedelta(seconds=15)).strftime("%H:%M:%S")
    insertDatesOnDay = datetime.time(0, 0, 1).strftime("%H:%M:%S")

# Токен для связи с ботом
bot = telebot.TeleBot(botkey)

def postpictureinchannel(listwithdates):
    # Данные для постинга
    date = listwithdates[0][1]
    print("Фотография с именем файла \n\t", date, "\nВ канал: \n\t", channelname)
    # Путь к картинке
    picpath = "database/photos/" + date
    # Открываем картинку для постинга
    photo = open(picpath, 'rb')
    # Отправляем картинку в канал
    try:
        bot.send_photo(channel_id, photo, caption = channelname)
    except Exception as exception:
        print("Произошла ошибка.\n\t", exception)

    print("Размер listwithdates: ", len(listwithdates))
    # Проверка на наличие оставшихся элементов
    if len(listwithdates) == 1:
        # Удаление первой строки
        listwithdates.pop(0)
        times.insertDatesOnDay = datetime.time(0, 0, 1).strftime("%H:%M:%S")
        print("На сегодня картинки кончились.")
    else:
        # Удаление первой строки
        listwithdates.pop(0)
        # Формирование нового времени постинга
        times.printPhoto = str(listwithdates[0][2])[11:]
        print("=========> Новое время постинга: ", times.printPhoto)

# Функция выяснения с какая фотография постится следующей
def searchnextphoto():
    global listwithdates
    # Достаём фаилы за сегодня из базы данных
    dates = datesfromtable()
    # Получаем дату и время сейчас
    timenow = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")

    elementsfordelete = 0
    for element in dates:
        if element[2] < timenow:
            elementsfordelete = elementsfordelete + 1
    elem = 0
    while (elem < elementsfordelete):
        del dates[0]
        elem = elem + 1

    listwithdates = dates
    if len(dates) == 0:
        print("Файлов в папке нет")
    else:
        times.printPhoto = str(dates[0][2])[11:]
        print("=========> Новое время постинга: ", times.printPhoto)

# Переменная где хранится список из базы данных
listwithdates = []

# Функция для выбора действия
def switcher(argument):
    global listwithdates
    match argument:
        case times.insertDatesOnDay:
            print("Данные на сегодня:")
            listwithdates = datesfromtable()
            for element in listwithdates:
                print("\t\t", element)
            # Формирование времени постинга первой картинки
            times.printPhoto = str(listwithdates[0][2])[11:]
            print("First time to posting: ", times.printPhoto)
        case times.printPhoto:
            print("Запуск функции постинга картинок.")
            print(listwithdates)
            postpictureinchannel(listwithdates)
        case _:
            print(argument)

# Функция выбора дествия каждую секунду
def eternalcycle():
    while True:
        # Время сейчас
        today = datetime.datetime.today()
        todaytime = today.strftime("%H:%M:%S")
        switcher(todaytime)
        time.sleep(0.5)

# Проверям наличие базы данных. Если база данных есть, то подключаемся, если нет, то создаём новую
# Путь до Базы Данных
pathdb = 'database\DataBase.db'
# Результат проверки наличия базы данных
result = os.path.exists(pathdb)
# Если база данных есть
if result is True:
    print("База данных есть. Поэтому запускаем функции для определения следующей картинки для постинга.")
    # Выясняем какая фотография должна поститься следующей
    searchnextphoto()
    # Запускаем вечный цикл обработки событий
    eternalcycle()
# Если базы данных нет, то инициализируем её и вставляем данные
else:
    initialdatabase()
    importphotos()
    eternalcycle()