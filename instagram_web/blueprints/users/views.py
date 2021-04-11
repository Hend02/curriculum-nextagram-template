from flask import Blueprint, render_template, redirect, request, session, flash, url_for
from flask_login import login_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models.user import User
from models.follow import Follow
from models.image import Image
from models.follow_request import FollowRequest
from helpers import s3

users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates')


@users_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('users/new.html')


@users_blueprint.route('/new_user', methods=['POST'])
def create():
    user = User(name=request.form.get("username"), email=request.form.get("email"), password=request.form.get("password"))
    if user.save():
        flash('You were successfully signed up!', 'success')
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.get(email = email)
        if user:
            result = check_password_hash(user.hash_password, password)
            if result:
                session["user_id"] = user.id
                login_user(user)
                return redirect(url_for("users.profile"))
    else:
        flash('Sign Up unsuccessful, Try again.', 'warning')
        flash('Password must be more than 6 characters.', 'warning')
        flash('Password must contain at least one Uppercase character.', 'warning')
        flash('Password must contain at least one Lowercase character.', 'warning')
        flash('Password must contain at least one Special character e.g("!""#""%""&""*"))', 'warning')
        return render_template("users/new.html")

@users_blueprint.route('/<id>', methods=["GET"])
def show(id):
    idol_id = id
    fan_request = User.select().join(FollowRequest, on=(User.id==FollowRequest.fan_request)).where(FollowRequest.idol_receive == User.get_by_id(id))
    fans = User.select().join(Follow, on=(User.id==Follow.fan)).where(Follow.idol == User.get_by_id(idol_id))
    user = User.get_by_id(id)
    return render_template('users/profile.html', user=user, fans=fans, follows=Follow, users=User, fan_request=fan_request)

@users_blueprint.route('/', methods=["GET"])
def index():
    return "USERS"

@users_blueprint.route("/profile", methods=["GET"])
@login_required
def profile():
    user = current_user
    return render_template('users/profile.html', user=user)

@users_blueprint.route('/edit', methods=['GET'])
@login_required
def edit():
    return render_template('users/edit.html', current_user=current_user)


@users_blueprint.route('/edit/<id>', methods=['POST'])
@login_required
def update(id):
    user = User.get_by_id(id)
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    private = request.form.get('private')
    unprivate = request.form.get('unprivate')
    if username:
        user.name = username
    if email:
        user.email = email
    if password:
        user.password = password
    if private:
        user.is_private = True
    if unprivate:
        user.is_private = False
    user.save()
    flash('Changes saved Successfully.', 'success')
    return redirect(url_for('users.edit', current_user=current_user))

@users_blueprint.route('/follow_request', methods=['GET'])
@login_required
def follow_request():
    fan_request = User.select().join(FollowRequest, on=(User.id==FollowRequest.fan_request)).where(FollowRequest.idol_receive == User.get_by_id(current_user.id))
    len_request = len(fan_request)
    return render_template('users/follow_request.html', current_user=current_user, fan_request=fan_request, len_request = len_request)