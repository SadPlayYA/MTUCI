from datetime import datetime
from random import randrange



# эта функция для вывода информации о фильме
def get_info_of_film():
    films = []
    for line in open('data/commands/films/name_films.txt', encoding='utf-8').readlines():
        line = line.replace('\n', '')
        films.append(line)
    index = randrange(0, len(films))
    
    return [get_info_for_commands(films[index]), films[index]]


# эта функция открывает отпределённый файл в зависимости от аргумента и возвращает содержимое. Аргумент - имя файла. ФУНКЦИЯ ДЛЯ ДИРЕКТОРИИ FILMS!!!
def get_info_for_commands(argument):
    return open(f'data/commands/films/{argument}/info.txt', encoding="utf-8").read()


# эта функция открывает отпределённый файл в зависимости от аргумента и возвращает содержимое. Аргумент - имя файла. ФУНКЦИЯ ДЛЯ БОТА!!!
def get_info_for_bot(argument='info'):
    temp = open(f'data/bot/{argument}.txt', encoding="utf-8").read()

    if argument == 'info':
        return f'{get_times_of_day()}\n\n{temp}'
    else:
        return temp


def get_name():
    return randrange(1,6)


# функция, которая выводит пожелание в зависимости от времени суток.
def get_times_of_day():
    current_datetime = datetime.now()
    hour = int(str(current_datetime.time())[:2])

    if 4 <= hour <= 11:
        return f'Доброе утро! 🙄'
    elif 12 <= hour <= 16:
        return f'Добрый день! 🙂'
    elif 15 <= hour <= 22:
        return f'Добрый вечер! ☺'
    else:
        return f'Доброй ночи! 🌚'


def emoji():
    content = open(f'data/commands/emoji/emojy.txt', encoding="utf-8").read().split()
    return content[randrange(0,len(content))]




