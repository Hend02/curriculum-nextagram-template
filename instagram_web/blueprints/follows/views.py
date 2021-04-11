from flask import Blueprint, render_template, redirect, request, session, flash, url_for
from flask_login import login_user, login_required, current_user
from models.user import User
from models.follow import Follow
from models.follow_request import FollowRequest
from helpers import s3

follows_blueprint = Blueprint('follows',
                            __name__,
                            template_folder='templates')

@follows_blueprint.route("/follows/<idol_id>/", methods=["POST"])
@login_required
def new(idol_id):
    idol = User.get_by_id(idol_id)
    fan = User.get_by_id(current_user.id)
    if idol.is_private == True:
        request = FollowRequest(fan_request = fan, idol_receive = idol)
        if request.save():
            flash('Follow Request has been Sent.', 'success')
            return redirect(url_for('users.show', id=idol_id))
    elif idol.is_private == False:
        follow = Follow(fan = fan, idol = idol )
        if follow.save():
            flash(f"You are now Following {idol.name}.", 'success')
            return redirect(url_for('users.show', id=idol_id))
    else:
        flash('Something went wrong. Please Try Again.', 'warning')
        return redirect(url_for('users.show', id=idol_id))

@follows_blueprint.route("/unfollows/<idol_id>/", methods=["POST"])
@login_required
def destroy(idol_id):
    idol = User.get_by_id(idol_id)
    fan = User.get_by_id(current_user.id)
    unfollow = Follow.get(fan = fan, idol = idol)
    if unfollow.delete_instance():
        flash(f"You have Unfollowed {idol.name}.", 'danger')
        return redirect(url_for('users.show', id=idol_id))

@follows_blueprint.route("/request_delete/<idol_id>/", methods=['POST'])
@login_required
def request_delete (idol_id):
    idol = User.get_by_id(idol_id)
    fan = User.get_by_id(current_user.id)
    del_request = FollowRequest.get(fan_request = fan, idol_receive = idol)
    if del_request.delete_instance():
        flash('Follow Request has been Deleted.', 'danger')
        return redirect(url_for('users.show', id=idol_id))

@follows_blueprint.route("/follows/request/<fan_id>", methods=["POST"])
@login_required
def accept_decline(fan_id):
    if request.form.get('accept'):
        fan = User.get_by_id(fan_id)
        idol = User.get_by_id(current_user.id)
        follow = Follow(fan = fan, idol = idol ) 
        del_request = FollowRequest.get(fan_request = fan, idol_receive = idol)
        if follow.save() and del_request.delete_instance():
            flash(f"{fan.name} is now following you.", 'success')
            return redirect(url_for('users.follow_request'))
    elif request.form.get('decline'):
        fan = User.get_by_id(fan_id)
        idol = User.get_by_id(current_user.id)
        del_request = FollowRequest.get(fan_request = fan, idol_receive = idol)
        if del_request.delete_instance():
            flash(f"You declined {fan.name} from following you.", 'danger')
            return redirect(url_for('users.follow_request'))

@follows_blueprint.route("/followers/<user_id>", methods=['GET'])
def followers(user_id):
    user = User.get_by_id(user_id)
    followers = User.select().join(Follow, on=(User.id==Follow.fan)).where(Follow.idol == User.get_by_id(user_id))
    length_followers = len(followers)
    # for follower in followers:
    #     print(follower)
    return render_template('/follows/followers.html', followers=followers, user=user, length_followers=length_followers)

@follows_blueprint.route("/following/<user_id>", methods=['GET'])
def following(user_id):
    user = User.get_by_id(user_id)
    following = User.select().join(Follow, on=(User.id==Follow.idol)).where(Follow.fan == User.get_by_id(user_id))
    length_following = len(following)
    # for follow in following:
    #     print(follow)
    return render_template("/follows/following.html", following=following, user=user, length_following=length_following)
