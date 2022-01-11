from flask import Flask, render_template, request, redirect
from config import db_name, user, passw, host
import psycopg2



app = Flask(__name__)
connection = psycopg2.connect(
            database=db_name,
            user=user,
            password=passw,
            host=host,
)
cursor = connection.cursor()


@app.route('/login/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':

        if request.form.get("login"):
            username = request. form.get('Login')
            password = request.form.get('Password')
            cursor.execute("SELECT * FROM person WHERE login=%s AND password=%s", (str(username), str(password)))
            records = cursor.fetchall()

            if len(username) == 0 or len(password) == 0:
                return 'Вы не ввели пароль или логин!'
            elif len(records) != 0:
                return render_template('account.html', full_name=records[0][0])
            else:
                return 'Вас нет в нашей базе данных или вы ввели неправильный логин или пароль. Проверьте правильность ' \
                       'введённых данных!'

        elif request.form.get("registration"):
            return redirect("/registration/")

    return render_template('login.html')


@app.route('/registration/', methods=['POST', 'GET'])
def registration():
    if request.method == 'POST':
        name = request.form.get('name')
        login = request.form.get('login')
        password = request.form.get('password')

        if len(str(name)) != 0 and len(str(login)) != 0 and len(str(password)) != 0:
            cursor.execute("SELECT login FROM person WHERE login='{}';".format(str(login)))
            req = cursor.fetchall()

            if req:
                return 'Мы не можем зарегистрировать. Такой пользователь уже существует!'
            else:
                cursor.execute('INSERT INTO person (full_name, login, password) VALUES (%s, %s, %s);',
                               (str(name), str(login), str(password)))
                connection.commit()

            return redirect('/login/')

        else:
            return 'Некорректные данные!'
        
    return render_template('registration.html')



if __name__ == "__main__":
    app.run(debug=False)

