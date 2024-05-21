from flask import Flask, url_for, redirect, render_template, request, Blueprint, flash, session
from flask_login import login_user, current_user, logout_user, login_required
from app_config import db, bcrypt
from models import User


users = Blueprint('users', __name__)


@users.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        user = User.query.filter_by(email=email).first()

        if user:
            flash('Email already exists', 'danger')

        if password != confirm_password:
            flash('Passwords do not match', 'danger')

        if len(password) < 6:
            flash('Password must be at least 6 characters', 'danger')

        if not user and len(password) >= 6 and password == confirm_password:
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            user = User(username=username, email=email, password=hashed_password, admin=False)
            db.session.add(user)
            db.session.commit()
            flash('Registration successful', 'success')
            return redirect(url_for('users.login'))

    return render_template('register.html')





@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            flash('Login successful', 'success')
            return redirect(url_for('main.home'))
        else:
            flash('Login unsuccessful. Please check your credentials', 'danger')
    return render_template('login.html')



@users.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))