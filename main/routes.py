# from flask import render_template, request, Blueprint
from flask import Flask, url_for, redirect, render_template, request, Blueprint, flash, session
from flask_login import login_user, current_user, logout_user, login_required
from app_config import db, bcrypt
from models import User


main = Blueprint('main', __name__)


@main.route('/')
@main.route('/index', methods=['GET', 'POST'])
def index():

    alert = session.pop('alert', None)
    bg_color = session.pop('bg_color', None)

    print(alert, bg_color)

    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        print(username, email, password, confirm_password)

        user = User.query.filter_by(email=email).first()

        if user:
            print('Email already exists')
            flash('Email already exists', 'danger')

        if password != confirm_password:
            print('Password does not match')
            flash('Passwords do not match', 'danger')

        if len(password) < 6:
            print('Password must be at least 6 characters')
            flash('Password must be at least 6 characters', 'danger')

        if not user and len(password) >= 6 and password == confirm_password:
            print('Registration successful, please log in.')
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            user = User(username=username, email=email, password=hashed_password, admin=False)
            db.session.add(user)
            db.session.commit()
            flash('Registration successful, please log in.'  'success')

            session['alert'] = 'Registration successful'
            session['bg_color'] = 'success'
            print('Registration successful, please log in. again')
            return redirect(url_for('main.index'))
    return render_template('index.html', alert=alert, bg_color=bg_color)






# Login
@main.route('/login', methods=['POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))


    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.password, password):
            print('Login successful')
            login_user(user, remember=True)

            session['alert'] = 'Login successful'
            session['bg_color'] = 'success'
        else:
            flash('Login unsuccessful. Please check username and password', 'danger')
            print('Login unsuccessful. Please check username and password')

            session['alert'] = 'Login unsuccessful. Please check username and password'
            session['bg_color'] = 'danger'
    return redirect(url_for('main.index'))



@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))