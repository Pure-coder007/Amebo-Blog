from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
import os
from sqlalchemy import create_engine
import pymysql, mysql.connector



secret_key =  'ssdfghjklreaertyuiytrewertyulhe3678oiytr43567iuiuytrewrtuyr3455'
app = Flask(__name__)

app.config['SECRET_KEY'] = secret_key
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/amebo?charset=utf8mb4'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)


login_manager.login_view = 'login'
login_manager.login_message_category = 'info'


from main.routes import main
from users.routes import users
from posts.routes import posts

app.register_blueprint(main)
app.register_blueprint(users)
app.register_blueprint(posts)
