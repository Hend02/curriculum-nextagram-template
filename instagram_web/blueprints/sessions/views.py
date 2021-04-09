from flask import Blueprint, render_template, redirect, request, session, flash, url_for
from flask_login.utils import login_required
from werkzeug.security import generate_password_hash, check_password_hash
from models.user import User
from flask_login import login_user, logout_user, current_user
from instagram_web.util.google_oauth import oauth

sessions_blueprint = Blueprint('sessions',
                            __name__,
                            template_folder='templates')


@sessions_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('sessions/new.html')

@sessions_blueprint.route('/new_user', methods=['POST'])
def create():
    email = request.form.get('email')
    password = request.form.get('password')
    user = User.get(email = email) 
    if user:
        result = check_password_hash(user.hash_password, password)
    
        if result:
            session["user_id"] = user.id
            flash("Signed In Successfully.", "success")
            login_user(user)
            return redirect(url_for("users.profile"))
        else:
            flash("Incorrect Credentials. Please try again.", "warning")
            return render_template("sessions/new.html")

@sessions_blueprint.route('/delete')
@login_required
def destroy():
    flash("Logged Out Successfully.", 'success')
    logout_user()
    return redirect(url_for('home'))

@sessions_blueprint.route("/google_login")
def google_login():
    redirect_uri = url_for('sessions.authorize', _external = True)
    return oauth.google.authorize_redirect(redirect_uri)

@sessions_blueprint.route("/authorize/google")
def authorize():
    oauth.google.authorize_access_token()
    email = oauth.google.get('https://www.googleapis.com/oauth2/v2/userinfo').json()['email']
    user = User.get_or_none(User.email == email)
    if user:
        login_user(user)
        flash('Logged In Successfully.', 'success')
        return redirect(url_for('users.profile'))
    else:
        flash('Invalid Account Details. Please Try Again.', 'warning')
        return redirect(url_for('sessions.new'))
