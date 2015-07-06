"""Main app, horrible code.
Create pr-s and issues when you see something wrong.
"""

__author__ = 'Fredrik A. Madsen-Malmo'

import os
import datetime
from flask import (Flask, g, flash, redirect, 
                    render_template, url_for)
from flask.ext.login import (LoginManager, login_user, 
                            logout_user, login_required,
                            current_user)
from flask.ext.bcrypt import check_password_hash

import languages

import models
import forms
from logic import get_lang_name, get_short_name

DEBUG = True
PORT = port = int(os.environ.get('PORT', 33507))
HOST = '0.0.0.0'

app = Flask(__name__)
app.secret_key = ';abrov]pwdjoeiw9g-20[34I)(U)*(&T%*^& \
                  %^$aay38794809#$xertcfhgvjkhbLVKGHFHGB]]]}{><?'

########### LOGIN MANAGER ############

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
	"""This is used by PeeWee to check if the user exists or not."""
	try:
		return models.User.get(models.User.id == user_id)
	except models.DoesNotExist:
		return None

######################################

###### BEFORE AND AFTER REQUEST ######

@app.before_request
def before_request():
    """Connect to db before each req"""
    g.db = models.DATABASE
    g.db.connect()
    g.user = current_user

@app.after_request
def after_request(response):
	"""Close the db connection after each req"""
	g.db.close()

	return response

######################################

############### ROUTES ###############

@app.route('/register', methods=['GET', 'POST'])
def register():
    logout_user()

    form = forms.RegisterForm()

    if form.validate_on_submit():
        flash('Registration complete.', 'success')

        models.User.create_user(
            username = form.username.data,
            password = form.password.data
        )

        login_user(models.User.get(models.User.username == form.username.data))

        flash('You are now logged in.', 'success')

        return redirect(url_for('index'))

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    logout_user()

    form = forms.LoginForm()

    if form.validate_on_submit():
        try:
            user = models.User.get(models.User.username == form.username.data)
        except models.DoesNotExist:
            flash('Your credentials are not correct', 'warning')
        else:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                flash('You are now logged in.', 'success')
                return redirect(url_for('index'))
            else:
                flash('Your credentials are not correct', 'warning')

    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()

    flash('You have been logged out successfully', 'info')

    return redirect(url_for('index'))

@app.route('/new_post', methods=['POST', 'GET'])
@login_required
def new_post():
    form = forms.PostForm()

    if form.validate_on_submit():
        try:
            models.Post.create(
                user=g.user._get_current_object(),
                content=form.content.data.strip(),
                language=form.language.data,
                display_language=get_lang_name(form.language.data)
            )

            flash('Snippet shared', 'success')
            return redirect(url_for('index'))
        except TypeError:
            raise 'Encountered error while posting'

    return render_template('new_post.html', form=form, LANGUAGES=languages.LANGUAGES)

@app.route('/<profile>', methods=['POST', 'GET'])
def profile(profile):
    try:
        user = models.User.get(models.User.username == profile)
    except Exception:
        return redirect(url_for('index'))

    stream = user.get_stream()

    user.followers = user.get_followers()
    user.following = user.get_following()

    try:
        if models.Relationship.get(from_user=g.user._get_current_object(), to_user=user):
            user.is_being_followed = True
    except Exception:
        user.is_being_followed = False

    return render_template('profile.html', stream=stream, user=user, LANGUAGES=languages.LANGUAGES)

@app.route('/')
def index():
    stream = models.Post.select().limit(100)

    return render_template('index.html', LANGUAGES=languages.LANGUAGES, stream=stream)

@app.route('/search/')
@app.route('/search/<query>', methods=['GET'])
def search(query=False):
    if not query:
        flash('Please enter a search query.', 'warning')
        return redirect(url_for('index'))

    if query in map(lambda x: x[1], languages.LANGUAGES):
        stream = (models.Post.select()
                    .where(models.Post.language == get_short_name(query))
                    .limit(100))
    else:
        stream = (models.Post.select()
                    .where(models.Post.content.contains(query))
                    .limit(100))

    return render_template('index.html', stream=stream, LANGUAGES=languages.LANGUAGES)

@app.route('/delete/<int:delete_id>', methods=['POST', 'GET'])
@login_required
def delete(delete_id):
    target = models.Post.get(models.Post.id == delete_id)

    if target.user == current_user:
        try:
            target.delete_instance()

            flash('Post successfully deleted', 'success')
            return redirect(url_for('index'))

        except IntegrityError:
            flash('Error occured while deleting post', 'warning')
            return redirect(url_for('index'))
    
    return redirect(url_for('index'))

@app.route('/edit/<int:edit_id>', methods=['POST', 'GET'])
@login_required
def edit(edit_id):
    target = models.Post.get(models.Post.id == edit_id)

    form = forms.PostForm()

    if target.user.username == current_user.username or current_user.is_admin:
        if form.validate_on_submit():
            try:
                models.Post.create(
                    timestamp=target.timestamp,
                    user=target.user,
                    content=form.content.data.strip(),
                    language=form.language.data,
                    display_language=get_lang_name(form.language.data)
                )

                target.delete_instance()

                flash('Snippet edited', 'success')
                return redirect(url_for('index'))

            except TypeError:
                flash('Encountered error while editing.', 'warning')
    
        form.content.data = target.content
        form.language.data = target.language

    return render_template('edit_post.html', form=form, post=target, LANGUAGES=languages.LANGUAGES)

@app.route('/<username>/follow', methods=['POST', 'GET'])
@login_required
def follow(username):
    try:
        to_user = models.User.get(models.User.username == username)
    except models.DoesNotExist:
        flash('Relationship does not exist.', 'warning')
        return redirect(url_for('profile', profile=username))

    try:
        models.Relationship.create(
            from_user = g.user._get_current_object(),
            to_user=to_user
        )
    except models.IntegrityError:
        pass
    else:
        flash('You are now following ' + to_user.username + '.', 'success')

    return redirect(url_for('profile', profile=username))

@app.route('/<username>/unfollow', methods=['POST', 'GET'])
@login_required
def unfollow(username):
    try:
        to_user = models.User.get(models.User.username == username)
    except models.DoesNotExist:
        flash('Could not unfollow {}'.username(username), 'warning')
        return redirect(url_for('profile', profile=username))

    try:
        models.Relationship.get(
            from_user = g.user._get_current_object(),
            to_user= to_user
        ).delete_instance()
        
        flash('You are no longer following ' + to_user.username + '.', 'success')
    except models.IntegrityError:
        flash('Could not unfollow {}'.username(username), 'warning')

    return redirect(url_for('profile', profile=username))

@app.route('/post/<int:post_id>', methods=['POST', 'GET'])
def post(post_id):
    stream = models.Post.select().where(models.Post.id == post_id)

    return render_template('post.html', stream=stream, LANGUAGES=languages.LANGUAGES)

@app.route('/<user>/edit', methods=['GET', 'POST'])
def edit_account(user):
    target = models.User.get(models.User.username == user)

    form = forms.EditUserForm()

    if target.username == current_user.username:
        if form.validate_on_submit():
            try:
                target.update(
                    password=models.generate_password_hash(form.password.data)
                ).execute()

                flash('Password changed.', 'success')
                return redirect(url_for('index'))

            except TypeError:
                flash('Encountered error while editing.', 'warning')

    elif current_user.is_admin:
        if form.validate_on_submit():
            try:
                target.password=models.generate_password_hash(form.password.data)
                target.save()

                flash('Password changed for user {}.'.format(target.username), 'success')
                return redirect(url_for('index'))

            except TypeError:
                flash('Encountered error while editing {}.'.format(target.username), 'warning')

    return render_template('edit_user.html', form=form, user=target, LANGUAGES=languages.LANGUAGES)

@app.route('/<user>/delete', methods=['POST', 'GET'])
def delete_account(user):
    target = models.User.get(models.User.username == user)

    if target.username == current_user.username or current_user.is_admin:
        try:
            for row in (models.Post.select()
                        .join(models.User)
                        .where(models.User.username == user)):
                row.delete_instance()

            target.delete_instance()

            flash('Account deleted, along with all posts.')
            return redirect(url_for('index'))
        except Exception:
            flash('Could not delete account.', 'warning')
            
            return redirect(url_for('index'))

######################################

if __name__ == '__main__':
    models.initialize()
    try:
        models.User.create_user('admin', 'admin', True)
    except Exception:
        pass

    app.run(debug=DEBUG, port=PORT, host=HOST)
