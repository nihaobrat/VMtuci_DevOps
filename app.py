from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.utils import secure_filename
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'

users = {} # Чтобы пост со страницы создания поста отправялся на страницу ленты
posts = []  # Список для хранения постов

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def home():
    return render_template('glavpage.html')

@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        login = request.form['login']
        name = request.form['name']
        surname = request.form['surname']
        email = request.form['email']
        password = request.form['password']

        if login in users:
            return "Логин уже занят", 400

        users[login] = {
            'name': name,
            'surname': surname,
            'email': email,
            'password': password
        }

        return redirect(url_for('signin'))

    return render_template('registration.html')

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']

        user = users.get(login)
        if user and user['password'] == password:
            # Успешный вход
            session['user'] = login
            return redirect(url_for('lenta'))

        else:
            return "Неверный логин или пароль", 401

    return render_template('signin.html')

@app.route('/lenta')
def lenta():
    if 'user' not in session:
        return redirect(url_for('signin'))

    user_data = users.get(session['user'], {})
    return render_template('lenta.html', posts=posts, user_data=user_data)


@app.route('/user_settings', methods=['GET', 'POST'])
def user_settings():
    if 'user' not in session:
        # Пользователь не вошел в систему, перенаправляем на страницу входа
        return redirect(url_for('signin'))

    user_data = users.get(session['user'])

    if request.method == 'POST':
        # Получаем данные из формы
        user_data['name'] = request.form.get('first-name')
        user_data['surname'] = request.form.get('last-name')
        # И так далее для каждого поля формы...

        # Здесь код для сохранения данных пользователя...
        users[session['user']] = user_data

        # После сохранения данных перенаправляем на страницу ленты или обратно на страницу настроек
        return redirect(url_for('lenta'))  # Или 'user_settings', если вы хотите остаться на этой странице

    # Если это GET-запрос, отображаем страницу настроек
    return render_template('user_settings.html', user_data=user_data)


@app.route('/createpost', methods=['GET', 'POST'])
def create_post():
    if 'user' not in session:
        return redirect(url_for('signin'))

    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        image = request.files.get('image')

        if image:
            image_filename = secure_filename(image.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
            image.save(image_path)
        else:
            image_filename = 'default.png'  # Или другое изображение по умолчанию

        post = {
            'author': users[session['user']]['name'],  # Предполагаем, что 'name' есть в данных пользователя
            'title': title,
            'content': content,
            'image_filename': image_filename,
            'timestamp': datetime.utcnow()  # Сохраняем текущее время
        }
        posts.append(post)
        return redirect(url_for('lenta'))

    return render_template('createpost.html')

@app.route('/createdpost')
def created_post():
    return render_template('createdpost.html')

@app.route('/welcome')
def welcome():
    return render_template('welcome.html')

if __name__ == '__main__':
    app.run(debug=True)
