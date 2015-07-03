"""This is the main app, this is basically where shit goes wrong 
when trying to publish the app to heroku.
"""

__author__ = 'Fredrik A. Madsen-Malmo'

from flask import (Flask, g, flash, redirect, 
                    render_template, url_for)
from flask.ext.login import (LoginManager, login_user, 
                            logout_user, login_required,
                            current_user)
from flask.ext.bcrypt import check_password_hash

import models
import forms
from logic import get_lang_name, get_short_name

DEBUG = True
PORT = 8080
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
    form = forms.RegisterForm()

    if form.validate_on_submit():
        flash('Registration complete.', 'success')

        model.User.create_user(
            username = form.username.data,
            password = form.password.data
        )

        return redirect_for(url_for('index'))

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = forms.LoginForm()

    if form.validate_on_submit():
        try:
            user = models.User.get(models.User.username == form.username.data)
        except models.DoesNotExist:
            flash('Your credentials are not correct', 'warning')
        else:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                flash('You are now logged in', 'info')
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

    return render_template('new_post.html', form=form)

@app.route('/<profile>')
def profile(profile):
    stream = (models.Post.select().where(
                models.Post.user == models.User.get(
                models.User.username == profile)))

    return render_template('profile.html', stream=stream)

@app.route('/')
def index():
    stream = models.Post.select().limit(100)

    return render_template('index.html', stream=stream)

@app.route('/delete/<timestamp>')
def delete(timestamp):
    models.Post.get().where(models.timestamp == timestamp).delete_instance()

@app.route('/search/')
@app.route('/search/<query>', methods=['GET'])
def search(query=False):
    if not query:
        flash('Please enter a search query.', 'warning')
        return redirect(url_for('index'))

    if query[0] == '@':
        stream = (models.Post.select()
                    .where(models.Post.language == get_short_name(query[1:]))
                    .limit(100))
    else:
        stream = (models.Post.select()
                    .where(models.Post.content.contains(query))
                    .limit(100))

    return render_template('index.html', stream=stream, get_lang_name=get_lang_name)

######################################

if __name__ == '__main__':
    models.initialize()
    try:
        models.User.create_user(
            username='MrMadsenMalmo',
            password='password', 
            admin=True
        )
        models.Post.create(
            user=models.User.get(models.User.username == 'MrMadsenMalmo'),
            content='console.log("Hello World!")',
            language='javascript',
            display_language=get_lang_name('javascript')
        )
    except ValueError:
        pass

	app.run(debug=DEBUG, port=PORT, host=HOST)