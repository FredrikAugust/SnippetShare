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
            email = form.email.data,
            password = form.password.data
        )

        return redirect_for(url_for('index'))

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = forms.LoginForm()

    if form.validate_on_submit():
        try:
            user = models.User.get(models.User.email == form.email.data)
        except models.DoesNotExist:
            flash('Your credentials are not correct', 'error')
        else:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                flash('You are now logged in', 'success')
                return redirect(url_for('index'))
            else:
                flash('Your credentials are not correct', 'error')

    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()

    flash('You have been logged out successfully')

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
                explanation=form.explanation.data.strip(),
                language=form.language.data
            )

            flash('Snippet shared', 'success')
            return redirect(url_for('index'))
        except TypeError:
            raise 'Encountered error while posting'

    flash('Please fill in all fields.')
    return redirect(url_for('index'))

@app.route('/')
def index():
    form = forms.PostForm()

    return render_template('index.html', form=form)

######################################

if __name__ == '__main__':
    models.initialize()
    try:
        models.User.create_user(
            email='mail.fredrikaugust@gmail.com', 
            password='password', 
            admin=True
        )
    except ValueError:
        pass

	app.run(debug=DEBUG, port=PORT, host=HOST)