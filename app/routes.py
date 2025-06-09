from flask import Blueprint, render_template, request, redirect, url_for, current_app
from flask_login import login_required, current_user
from .models import Task
from . import db

main = Blueprint('main', __name__)

@main.route('/')
@login_required
def index():
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    current_app.logger.info(f"User '{current_user.username}' accessed the task list.")
    return render_template('index.html', tasks=tasks)

@main.route('/add', methods=['POST'])
@login_required
def add():
    content = request.form['content']
    task = Task(content=content, user_id=current_user.id)
    db.session.add(task)
    db.session.commit()
    current_app.logger.info(f"User '{current_user.username}' added task: {content}")
    return redirect(url_for('main.index'))

@main.route('/delete/<int:id>')
@login_required
def delete(id):
    task = Task.query.get_or_404(id)
    current_app.logger.info(f"User '{current_user.username}' deleted task: {task.content}")
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('main.index'))
