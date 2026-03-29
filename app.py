from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Task

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-key-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Create database tables
with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        task_content = request.form['content'].strip()
        if task_content:
            new_task = Task(content=task_content)
            try:
                db.session.add(new_task)
                db.session.commit()
                flash('Task added successfully!', 'success')
            except:
                flash('There was an issue adding your task.', 'error')
        else:
            flash('Task cannot be empty.', 'error')
        return redirect(url_for('index'))

    tasks = Task.query.order_by(Task.date_created.desc()).all()
    return render_template('index.html', tasks=tasks)

@app.route('/complete/<int:task_id>')
def complete(task_id):
    task = Task.query.get_or_404(task_id)
    task.completed = not task.completed
    db.session.commit()
    flash('Task updated!', 'success')
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>')
def delete(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    flash('Task deleted!', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
