from flask import render_template, url_for, redirect, request, Blueprint, abort
from flask_login import login_required, current_user
from app_config import db
from models import User
from models import Post
import cloudinary
import cloudinary.uploader

posts = Blueprint('posts', __name__)

@posts.route('/single_post', methods=['GET', 'POST'])
def single_post():
    return render_template('single_post.html')





@posts.route('/create_post', methods=['GET', 'POST'])
@login_required
def create_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        image = request.form['image']

        post = Post(title=title, content=content, image=image, author=current_user)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('main.index'))
    
    return render_template('create_post.html')