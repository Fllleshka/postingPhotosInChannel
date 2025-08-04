from classes import database, work

if __name__ == '__main__':
    #os.remove("database/DataBase.db")
    # Создаём экземпляр класса базы данных
    dbase = database()
    # Проверка на наличие базы данных
    if dbase.checkdatabase() is True:
        pass
    else:
        # Создаём базу данных
        dbase.initialdatabase()
        # Формируем список картинок для постинга и записываем в базу
        dbase.importimages()
        # Формируем список видео для постинга и записываем в базу
        dbase.importvideos()
    # Создаём экземпляр класса work
    dbase = work()
    #dbase.postpictureinchannel()
    # Функция бесконечного таймера с интервалом 1 секунда
    dbase.eternalcycle()