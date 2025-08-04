import datetime

class times:
    # Время функции печати
    printPhoto = (datetime.datetime.today() +
                  datetime.timedelta(seconds=25)).strftime("%H:%M:%S")


    # Время выяснения данных для постинга
    #insertDatesOnDay = datetime.time(0, 0, 1).strftime("%H:%M:%S")
    insertDatesOnDay = (datetime.datetime.today() +
                  datetime.timedelta(seconds=20)).strftime("%H:%M:%S")
