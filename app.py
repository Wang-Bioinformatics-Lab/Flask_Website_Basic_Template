# app.py
import os

from flask import Flask
from peewee import SqliteDatabase

APP_ROOT = os.path.dirname(os.path.realpath(__file__))
DATABASE = os.path.join(APP_ROOT, './database/database.db')

class CustomFlask(Flask):
  jinja_options = Flask.jinja_options.copy()
  jinja_options.update(dict(
    block_start_string='(%',
    block_end_string='%)',
    variable_start_string='((',
    variable_end_string='))',
    comment_start_string='(#',
    comment_end_string='#)',
  ))

app = CustomFlask(__name__)
app.config.from_object(__name__)
db = SqliteDatabase(app.config['DATABASE'], pragmas=[('journal_mode', 'wal')])

app.config['UPLOAD_FOLDER'] = './tempuploads'

try:
    os.mkdir(app.config['UPLOAD_FOLDER'])
except:
    print("Cannot Create", app.config['UPLOAD_FOLDER'])

from flask_login import LoginManager, UserMixin
app.secret_key = os.environ['SECRET_KEY'] # reading from env variable
login_manager = LoginManager()
login_manager.init_app(app)

# Predefined users from env
users = {'admin':{'pw': os.environ['ADMIN_PW']}}

class User(UserMixin):
  pass

@login_manager.user_loader
def user_loader(username):
  if username not in users:
    return

  user = User()
  user.id = username
  return user

@login_manager.request_loader
def request_loader(request):
  username = request.form.get('username')
  if username not in users:
    return

  user = User()
  user.id = username

  user.is_authenticated = request.form['pw'] == users[username]['pw']

  return user