from flask import render_template, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
from models import Todo, db, User

class TodoController():
  def index():
    if 'user_id' not in session:
      return redirect('/login')
    user_id = session['user_id']
    todos = Todo.query.filter_by(user_id=user_id).all()
    return render_template('index.html', todos=todos)

  def create():
    if 'user_id' not in session:
      return redirect('/login')
    user_id = session['user_id']

    title = request.form.get('title')
    new_todo = Todo(title=title, complete=False, user_id=user_id)
    db.session.add(new_todo)
    db.session.commit()
    return redirect('/')

  def delete(id):
    if 'user_id' not in session:
      return redirect('/login')
    todo = Todo.query.filter_by(id=id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')

  def complete(id):
    if 'user_id' not in session:
      return redirect('/login')
    todo = Todo.query.filter_by(id=id).first()
    todo.complete = True
    db.session.commit()
    return redirect('/')

  def update(id):
    if 'user_id' not in session:
      return redirect('/login')
    title = request.form.get('title')
    todo = Todo.query.filter_by(id=id).first()
    todo.title = title
    db.session.commit()
    return redirect('/')

class UserController():
  def login():
    return render_template('login.html')

  def signin():
    email = request.form.get('email')
    password = request.form.get('password')
    user = User.query.filter_by(email=email).first()
    if not user:
      return redirect('/login')
    if not check_password_hash(user.password, password):
      return redirect('/login')
    session['user_id'] = user.id
    return redirect('/')

  def register():
    return render_template('register.html')

  def signup():
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    user = User.query.filter_by(email=email).first()
    if user:
      return redirect('/register')
    new_user = User(
      name=name,
      email=email,
      password=generate_password_hash(password, method='sha256')
    )
    db.session.add(new_user)
    db.session.commit()
    return redirect('/login')

  def logout():
    if 'user_id' in session:
      session.pop('user_id', None)
    return redirect('/login')