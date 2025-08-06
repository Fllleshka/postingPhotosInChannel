import os.path
import sqlite3
import datetime
import random
import time
import telebot
import tqdm
from times import times
from threading import Thread

from dates import botkey, namechannel, idchannel

class database:
    def __init__(self):
        # Путь до Базы Данных
        self.pathdatabase = 'database/DataBase.db'
        # Путь до папки с картинками
        self.imagesfolder = "photos/"
        # Путь до папки с видео
        self.videosfolder = "video_files/"

    # Инициализация базы данных
    def initialdatabase(self):
        # Открываем соединение с базой данных
        con = sqlite3.connect(self.pathdatabase)
        # Создаём таблицу постинга картинок
        with con:
            con.execute(
                """
                    CREATE TABLE IMAGES (
                        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                        name_pic TEXT,
                        time_to_post datetime
                    );
                """
            )
        # Создаём таблицу постинга видео
        with con:
            con.execute(
                """
                    CREATE TABLE VIDEOS (
                        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                        name_video TEXT,
                        time_to_post datetime
                    );
                """
            )
        # Создаём таблицу постинга рекламы
        with con:
            con.execute(
                """
                    CREATE TABLE PROMOTION (
                        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                        name_media TEXT,
                        text_media TEXT,
                        time_to_post datetime
                    );
                """
            )
        # Закрываем соединение с базой данных
        con.close()

    # Проверка и создание базы данных
    def checkdatabase(self):
        result = os.path.exists(self.pathdatabase)
        today = datetime.datetime.today()
        todaytime = today.strftime("%H:%M:%S")
        if result is True:
            print(f"{todaytime} База данных есть.")
            return True
        else:
            print(f"{todaytime} Надо создать новую базу данных.")
            return False

    # Заполнение данных в таблице картинки
    def importimages(self):
        # Проверка картинок на повторы
        self.checkfolderforduplicate(self.imagesfolder)
        # Открываем соединение с базой данных
        con = sqlite3.connect(self.pathdatabase)
        # Данные для базы данных
        sql = 'INSERT INTO IMAGES (id, name_pic, time_to_post) values(?,?,?)'
        dates = []
        # Импортируем данные по картинкам
        files = os.listdir(self.imagesfolder)
        random.shuffle(files)
        index = 0
        # Пробегаемся по элементам в списке
        timetopost = datetime.datetime.today()
        for element in tqdm.tqdm(files):
            index += 1
            timetopost2 = datetime.timedelta(minutes = random.randint(10, 20), seconds = random.randint(1, 60))
            timetopost += timetopost2
            fullpathfolder = self.imagesfolder + element
            dates.append((index, fullpathfolder, timetopost.strftime("%Y-%m-%d %H:%M:%S")))
        with con:
            con.executemany(sql, dates)
        con.close()

    # Заполнение данных в таблице видео
    def importvideos(self):
        # Проверка видео на повторы
        self.checkfolderforduplicate(self.videosfolder)
        # Открываем соединение с базой данных
        con = sqlite3.connect(self.pathdatabase)
        # Данные для базы данных
        sql = 'INSERT INTO VIDEOS (id, name_video, time_to_post) values(?,?,?)'
        dates = []
        # Импортируем данные по картинкам
        files = os.listdir(self.videosfolder)
        random.shuffle(files)
        index = 0
        # Пробегаемся по элементам в списке
        timetopost = datetime.datetime.today()
        for element in tqdm.tqdm(files):
            index += 1
            timetopost2 = datetime.timedelta(minutes = random.randint(10, 20), seconds = random.randint(1, 60))
            timetopost += timetopost2
            fullpathfolder = self.videosfolder + element
            dates.append((index, fullpathfolder, timetopost.strftime("%Y-%m-%d %H:%M:%S")))
        with con:
            con.executemany(sql, dates)
        con.close()

    # Проверка папок на повторы
    def checkfolderforduplicate(self, path):
        listdir = os.listdir(path)
        print(f"Количество файлов в папке [{path}]: {len(listdir)}")
        time.sleep(5)
        for element in tqdm.tqdm(listdir):
            if "thumb" in element or "(1)" in element:
                pathtofile = path + element
                #print(f"{element} необходимо удалить. Путь [{pathtofile}] доступность [{os.path.exists(self.pathdatabase)}]")
                os.remove(pathtofile)

class work(database):
    def __init__(self):
        # Вызов конструктора родительского класса
        super().__init__()
        self.botkey = botkey
        self.namechennel = namechannel
        self.listdatesonday = None
        self.idchannel = idchannel

    # Функция выбора действия каждую секунду
    def eternalcycle(self):
        while True:
            # Время сейчас
            today = datetime.datetime.today()
            todaytime = today.strftime("%H:%M:%S")
            self.switcher(todaytime)
            time.sleep(0.5)

    # Функция импорт данных из таблицы
    def detesfromtable(self):
        # Соединение с базой данных
        con = sqlite3.connect(self.pathdatabase)
        today = datetime.datetime.today()
        todayday = today.strftime("%Y-%m-%d")
        print(times.insertDatesOnDay)
        print(datetime.time(0, 0, 1).strftime("%H:%M:%S"))
        print(times.insertDatesOnDay != datetime.time(0, 0, 1).strftime("%H:%M:%S"))

        if times.insertDatesOnDay != datetime.time(0, 0, 1).strftime("%H:%M:%S"):
            starttime = today.strftime("%Y-%m-%d %H:%M:%S")
        else:
            starttime = todayday + " 00:00:01"

        endtime = todayday + " 23:59:59"
        # Запрос к базе данных на формирование данных по всем запланированным постам на сегодня
        query = (("SELECT * FROM IMAGES WHERE time_to_post >= '") +
                 starttime + "' and time_to_post <= '" + endtime +
                 "' UNION SELECT * FROM VIDEOS WHERE time_to_post >= '" +
                 starttime + "' and time_to_post <= '" + endtime + "' ORDER BY time_to_post ASC")
        print(query)
        with con:
            data = con.execute(query).fetchall()
        con.close()
        return data

    # Функция для выбора действия
    def switcher(self, argument):
        match argument:
            case times.insertDatesOnDay:
                print("Данные на сегодня:")
                self.listdatesonday = self.detesfromtable()
                for element in self.listdatesonday:
                    print("\t\t", element)
                # Формирование времени постинга первой картинки
                times.printPhoto = str(self.listdatesonday[0][2])[11:]
                print("Первое время для постинга: ", times.printPhoto)
                # Приведение времени импорта в соответствие
                times.insertDatesOnDay = datetime.time(0, 0, 1).strftime("%H:%M:%S")
            case times.printPhoto:
                print("Запуск функции постинга картинок.")
                thread = Thread(target = self.postpictureinchannel)
                thread.start()
            case _:
                print(argument)

    # Функция постинга картинок в канал
    def postpictureinchannel(self):
        # Путь к картинке
        date = self.listdatesonday[0][1]
        print("Фотография с именем файла \n\t", date, "\nВ канал: \n\t", self.namechennel)
        # Открываем картинку для постинга
        media = open(date, 'rb')
        # Отправляем картинку в канал
        bot = telebot.TeleBot(botkey)
        try:
            print(date, type(date))
            if "photos" in date:
                bot.send_photo(self.idchannel, media, caption=self.namechennel)
            else:
                bot.send_animation(self.idchannel, media, caption=self.namechennel)
        except Exception as exception:
            print("Произошла ошибка.\n\t", exception)

        print("Размер массива с данными: ", len(self.listdatesonday))
        # Проверка на наличие оставшихся элементов
        if len(self.listdatesonday) == 1:
            # Удаление первой строки
            self.listdatesonday.pop(0)
            times.insertDatesOnDay = datetime.time(0, 0, 1).strftime("%H:%M:%S")
            print("На сегодня картинки кончились.")
        else:
            # Удаление первой строки
            self.listdatesonday.pop(0)
            # Формирование нового времени постинга
            times.printPhoto = str(self.listdatesonday[0][2])[11:]
            print("=========> Новое время постинга: ", times.printPhoto)