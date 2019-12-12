from app import app, db
from flask import render_template, flash, redirect, url_for, request
from app.forms import LoginForm, RegistrationForm, EditProfileForm, PostForm
from app.models import User, Post
from flask_login import current_user, login_user, logout_user, login_required
from hashlib import md5
from datetime import datetime


# explore function
@app.route('/explore')
def explore():
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    print(posts)
    return render_template('index.html', title='explore', posts=posts)


# before view function
@app.before_request
def before_request():
    if(current_user.is_authenticated):
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

# User view function
@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    posts = user.posts.order_by(Post.timestamp.desc()).paginate(
        page, app.config['POSTS_PER_PAGE'], False)
    if posts.has_next:
        next_url = url_for('user', username=username, page=posts.next_num)
    else:
        next_url = None
    print(next_url)

    if posts.has_prev:
        prev_url = url_for('user', username=username, page=posts.prev_num)
    else:
        prev_url = None
    print(next_url)

    return render_template('user.html', user=user, posts=posts.items, prev_url=prev_url, next_url=next_url)

# Basic view aka Home
@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = PostForm()
    if(form.validate_on_submit()):
        post = Post(body=form.post.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post is now live!')
        return redirect(url_for('index'))
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=current_user.username).first_or_404()
    posts = current_user.followed_posts().paginate(
        page, app.config['POSTS_PER_PAGE'], False)
    if posts.has_next:
        next_url = url_for('index', page=posts.next_num)
    else:
        next_url = None
    print(next_url)

    if posts.has_prev:
        prev_url = url_for('index', page=posts.prev_num)
    else:
        prev_url = None
    print(next_url)

    return render_template('index.html', title='what just the times', user=user, posts=posts.items, form=form, next_url=next_url, prev_url=prev_url)

# login view
@app.route('/login', methods=['GET', 'POST'])
def login():
    if(current_user.is_authenticated):
        return redirect(url_for('index'))
    form = LoginForm()
    if(form.validate_on_submit()):
        user = User.query.filter_by(username=form.username.data).first()
        if(user is None or not user.check_password(form.password.data)):
            flash('Invalid user or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        flash('LOGIN REQUESSTED FOR USER {}'.format(form.username.data))
        return redirect(url_for('index'))
    return render_template('login.html', title="Login", form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
# Regisration page view
@app.route('/register', methods=['GET', 'POST'])
def register():
    if(current_user.is_authenticated):
        return redirect(url_for('index'))
    form = RegistrationForm()
    if(form.validate_on_submit()):
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))

    return render_template('register.html', title='Register', form=form)


# Edit form
@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Change has been saved')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile', form=form)

# view for follow
@app.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()

    if(user is None):
        flash('User {} not found'.format(username))
        return redirect(url_for('index'))
    if user == current_user:
        flash('You Cannot follow yourself!')
        return redirect(url_for('user', username=username))
    current_user.follow(user)
    db.session.commit()
    flash('You are following {}!'.format(username))
    return redirect(url_for('user', username=username))

# view for unfollow
@app.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()

    if(user is None):
        flash('User {} not found'.format(username))
        return redirect(url_for('index'))
    if user == current_user:
        flash('You Cannot unfollow yourself!')
        return redirect(url_for('user', username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash('You are not following {}!'.format(username))
    return redirect(url_for('user', username=username))


# user_profile pop_up
@app.route('/user/<username>/popup')
@login_required
def user_popup(username):
    user = User.query.filter_by(username=username).first_or_404()
    print(user)
    return render_template('user_popup.html',user=user)