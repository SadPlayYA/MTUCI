import psycopg2
import telebot
from config import database_name, user, password, host, token
from command import times_of_day, get_week



def get_data(params1, params2=1, params3=1):
    # params1 - even and odd weeks. 1 - odd, 0 - even
    # params2 - for the whole week or not. 1 - whole week, 0 - not
    # params3 - for the current week or next. 0 - current, 1 - next
    try:
        # set the necessary parameters for connecting to the database
        connection = psycopg2.connect(
            database=database_name,
            user=user,
            password=password,
            host=host
        )
        # cursor required to interact with database
        cursor = connection.cursor()
        print('[INFO] PostgreSQL is connection.')
        # if you are asked to display the schedule for the week
        if params2 == 1:

            # if you are asked to display the schedule for the next week
            if params3 == 1:
                if params1 == 1:
                    params1 = 0

                # in the current week
                else:
                    params1 = 1

            # determine which table to open for the timetable (for even or odd)
            if params1 == 0:
                params1 = "_even"
            else:
                params1 = "_odd"

            # requests to the database
            cursor.execute(f"SELECT * FROM personal.timetable{params1}")

            # store the resulting list in a variable
            data_timetable = cursor.fetchall()

            # the list we will return
            returned_items = []

            # data_timetable[index] when index = 0 for Monday, index = 1 for Tuesday ... index = 4 for Friday, index = 5 for Saturday
            # we go through the loop on each day, that is, on each line
            for item in data_timetable:
                # get day of the week
                date = item[0]

                # determinate the line, which we will send to returned_items
                finaly_day_table = f'[{date}]\n------------------------------------------------------------\n'

                # we go through the cycle on each subject, getting the necessary data from the database
                for index in range(1,6):
                    # in this situation, index is not just the index of the list, but the sequence number of the pair. So great coincidence, isn't it?

                    # get subject
                    subject = item[index]

                    # if pair is NONE, then there is nothing
                    # '-' - this means that there is no pair

                    # in case there is a pair
                    if subject != '-':
                        # from the database we get the full name of the teacher and the location of the lesson
                        cursor.execute("SELECT teacher, place FROM personal.subjects WHERE subject='{}'".format(subject))

                        # push the received data from the database into a temporary variable
                        temp = cursor.fetchone()

                        # we get the full name of the teacher and the place of the lesson
                        teacher, place = temp[0], temp[1]

                        # get the class time from the database and save it to a variable
                        cursor.execute("SELECT time FROM personal.time_pair WHERE pair = {}".format(index))
                        time = cursor.fetchone()[0]

                        # concatenate the parts into the required format
                        finaly_day_table += f'[{index}] \n>> [Предмет] - {subject} \n>> [Место] - {place} \n>> [Время] - {time} \n>> [Преподаватель] - {teacher} \n\n'

                    # in case there is no pair
                    else:
                        # concatenate the parts into the required format if there is no pair
                        finaly_day_table += f'[{index}] \n>> Пара отсутствует. \n\n'

                # at the end of each iteration of the iteration, add the resulting string to the returned list
                returned_items.append(finaly_day_table)

        # at the end of the iteration, return the returned list
        return returned_items

    except Exception as _ex:
        print('[INFO] Pop out errors while working with PostgreSQL ', _ex)

    finally:
        if connection:
            cursor.close()
            connection.close()
            print('[INFO] PostgreSQL connection closed.')


# create object 'bot'
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def start(message):
    keyboard = telebot.types.ReplyKeyboardMarkup()
    keyboard.row('Расписание', '/week', '/mtuci', '/help')
    bot.send_message(message.chat.id, f'{times_of_day()}\nВыберите необходимую команду:', reply_markup=keyboard)
    print('[INFO] The function "start" ended the work ')


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id,
                     'Я бот, который присылает расписание. Вот что я умею:\n\n/week - подскажу, какая сейчас неделя (чётная или нечётная).'
                     f'\n/mtuci - прекрасное место, где учится мой создатель.\n/help - помощь, если что-то не понятно.\n\nТакже я умею присылать расписание.')
    print('[INFO] The function "help" ended the work ')


@bot.message_handler(commands=['week'])
def week(message):
    if get_week() == 0:
        bot.send_message(message.chat.id, 'На данный момент чётная неделя!')
    else:
        bot.send_message(message.chat.id, 'На данный момент нечётная неделя!')
    print('[INFO] The function "week" ended the work ')


@bot.message_handler(commands=['mtuci'])
def mtuci(message):
    bot.send_message(message.chat.id, 'Cсылка на официальный сайт МТУСИ – https://mtuci.ru/')
    print('[INFO] The function "mtuci" ended the work ')


@bot.message_handler(content_types=['text'])
def timetable(message):
    if message.text.lower() == 'расписание':
        keyboard = telebot.types.ReplyKeyboardMarkup()
        keyboard.row('Выбрать день', 'Расписание на текущую неделю', 'Расписание на следующую неделю',
                     'Назад в главное меню')
        bot.send_message(message.chat.id, 'Что дальше?', reply_markup=keyboard)
        print('[INFO] The function "расписание" ended the work ')

    elif message.text.lower() == 'назад в главное меню':
        keyboard = telebot.types.ReplyKeyboardMarkup()
        keyboard.row('Расписание', '/week', '/mtuci', '/help')
        bot.send_message(message.chat.id, 'Выберите необходимую команду:', reply_markup=keyboard)
        print('[INFO] The function "назад в главное меню" ended the work ')

    elif message.text.lower() == 'выбрать день':
        keyboard = telebot.types.ReplyKeyboardMarkup()
        keyboard.row('Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Вернуться назад')
        bot.send_message(message.chat.id, 'Выберите интересующий вас день:', reply_markup=keyboard)
        print('[INFO] The function "выбрать день" ended the work ')

    elif message.text.lower() == 'вернуться назад':
        keyboard = telebot.types.ReplyKeyboardMarkup()
        keyboard.row('Выбрать день', 'Расписание на текущую неделю', 'Расписание на следующую неделю',
                     'Назад в главное меню')
        bot.send_message(message.chat.id, 'Что дальше?', reply_markup=keyboard)
        print('[INFO] The function "вернуться назад" ended the work ')

    elif message.text.lower() == 'расписание на текущую неделю':
        try:
            rezult = get_data(get_week(), 1, 0)
            for item in rezult:
                bot.send_message(message.chat.id, item)
        finally:
            print('[INFO] The function "расписание на текущую неделю" ended the work ')


    elif message.text.lower() == 'расписание на следующую неделю':
        try:
            rezult_list = get_data(get_week(), 1, 1)
            for item in rezult_list:
                bot.send_message(message.chat.id, item)
        finally:
            print('[INFO] The function "расписание на слудующую неделю" ended the work ')

    elif message.text.lower() in ['понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота']:
        try:
            dict = {'понедельник': 0, 'вторник': 1, 'среда': 2, 'четверг': 3, 'пятница': 4, 'суббота': 5}
            value = dict.get(message.text.lower())
            bot.send_message(message.chat.id, get_data(get_week(), 1, 0)[value])
        finally:
            print('[INFO] The function "расписание на выбранный день" ended the work ')

    else:
        bot.send_message(message.chat.id, "I'm sorry, I did not understand you.")



# for the bot to work
bot.polling()
