from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/home')
def home():
    return render_template("home.html", user=current_user)

@auth.route('/download')
def download():
    return render_template("download.html", user=current_user)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')
        
        user = User.query.filter_by(login=login).first()
        if user:
            print(user.password, password)
            if check_password_hash(user.password, password):
                flash('Авторизация прошла успешно!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.cabinet'))
            else:
                flash('Неверный пароль, попробуйте снова', category='error')
        else:
            flash('Данного логина не существует', category='error')

    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        login = request.form.get('login')
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        login_check = User.query.filter_by(login=login).first()
        email_check = User.query.filter_by(email=email).first()
        if login_check:
            flash('Данный логин уже зарегистрирован', category='error')
        elif email_check:
            flash('Данная почта уже зарегистрирована', category='error')
        elif len(login) < 4:
            flash('Логин должен быть больше 4 символов', category='error')
        elif len(email) < 4:
            flash('Почта должна быть больше 4 символов', category='error')
        elif password1 != password2:
            flash('Пароли должны совпадать', category='error')
        elif len(password1) < 8:
            flash('Пароль должен включать в себя не менее 8 символов', category='error')
        else:
            new_user = User(login=login, email=email, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Аккаунт создан!', category='success')
            return redirect(url_for('views.home'))

    return render_template("register.html", user=current_user)