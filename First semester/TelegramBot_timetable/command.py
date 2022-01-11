from datetime import datetime



def get_week():
    date_now = datetime.now()
    date_countdown = datetime(2021, 8, 30)
    difference = date_now - date_countdown
    week = difference.days // 7 + 1
    # 1 - odd week, 0 - even week
    return week % 2


def times_of_day():
    date_time = datetime.now()
    hour = int(str(date_time.time())[:2])

    if 4 <= hour <= 11:
        return f'Доброе утро! 🙄'
    elif 12 <= hour < 16:
        return f'Добрый день! 🙂'
    elif 16 <= hour < 23:
        return f'Добрый вечер! ☺'
    else:
        return f'Доброй ночи! 🌚'
    
