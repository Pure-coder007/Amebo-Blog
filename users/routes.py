from flask import Flask, url_for, redirect, render_template, request, Blueprint, flash, session
from flask_login import login_user, current_user, logout_user, login_required
from app_config import db, bcrypt
from models import User, Post
from datetime import datetime
import cloudinary
import cloudinary.uploader
from werkzeug.utils import secure_filename


users = Blueprint('users', __name__)


cloudinary.config(
    cloud_name = "duyoxldib",
    api_key = "778871683257166", 
  api_secret = "NM2WHVuvMytyfnVziuzRScXrrNk"
)


app = Flask(__name__)
app.secret_key = 'asdfghjklpoiuytrewqasdfghjklkjhgfdssdftyuikjhgfdsdertyuil'

app.config['UPLOADED_PHOTOS_DEST'] = 'static/assets/img'



@users.route('/create_post', methods=['GET', 'POST'])
@login_required
def create_post():
    if not current_user.admin:
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        date_posted = datetime.now()
        image = request.files.get('image')
        user_id = current_user.id

        if image:
            filename = secure_filename(image.filename)
            response = cloudinary.uploader.upload(image, public_id=f"posts/{filename}")
            image = response['secure_url']

        post = Post(title=title, content=content, date_posted=date_posted, image=image, user_id=user_id)
        db.session.add(post)
        db.session.commit()
        flash('Post created successfully', 'success')
        return redirect(url_for('main.index'))
    return render_template('create_post.html')





# Dispaly all posts
@users.route('/posts', methods=['GET', 'POST'])
@login_required
def posts():
    posts = Post.query.order_by(Post.date_posted.desc()).all()
    return render_template('index.html', posts=posts)