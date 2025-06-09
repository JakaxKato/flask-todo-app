from flask import Blueprint, render_template, redirect, url_for, request, flash
from .models import User
from . import db, login_manager
from flask_login import login_user, logout_user, login_required

auth = Blueprint('auth', __name__)

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and user.check_password(request.form['password']):
            login_user(user)
            return redirect(url_for('main.index'))
        flash('Invalid credentials')
    return render_template('login.html')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password'].strip()

        # Validasi input sederhana
        if not username or not password:
            flash("Username dan password tidak boleh kosong.")
            return redirect(url_for('auth.register'))

        if len(password) < 6:
            flash("Password minimal 6 karakter.")
            return redirect(url_for('auth.register'))

        # Cek duplikasi username
        if User.query.filter_by(username=username).first():
            flash("Username sudah digunakan.")
            return redirect(url_for('auth.register'))

        new_user = User(username=username)
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('auth.login'))

    return render_template('register.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
