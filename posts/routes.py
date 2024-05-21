from flask import render_template, url_for, redirect, request, Blueprint, abort
from flask_login import login_required, current_user
from app_config import db
from models import User

posts = Blueprint('posts', __name__)

@posts.route('/single_post', methods=['GET', 'POST'])
def single_post():
    return render_template('single_post.html')