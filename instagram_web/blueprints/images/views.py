from flask import Blueprint, render_template, redirect, request, session, flash, url_for
from flask_login import login_user, login_required, current_user
from models.image import Image
from models.user import User
from helpers import s3

images_blueprint = Blueprint('images',
                            __name__,
                            template_folder='templates')


@images_blueprint.route("/upload", methods=["GET"])
@login_required
def upload():
    return render_template('images/new.html', current_user=current_user)

@images_blueprint.route("/upload_profile/<id>", methods=["POST"])
@login_required
def upload_image(id):
    if "image" not in request.files:
        flash("No Image selected", "warning")
        return redirect(url_for('images.upload'))
    else:
        file = request.files['image']
        bucket_name = "nextagram-aws-bucket"
        s3.upload_fileobj(
            file,
            bucket_name,
            file.filename,
            ExtraArgs={
                "ACL": "public-read",
                "ContentType": file.content_type
            }
        )
        user = User.get_by_id(id)
        user.profile_image = f"https://{bucket_name}.s3-ap-southeast-1.amazonaws.com/{file.filename}"
        if user.save():
            flash("Profile Picture Uploaded Successfully", "success")
            return redirect(url_for('users.profile'))
        else:
            flash("Something Went Wrong.", 'danger')
            return render_template("images/new.html")

@images_blueprint.route('/upload/images/<id>', methods=["POST"])
@login_required
def upload_images(id):
    user  = User.get_by_id(id)
    if "image" not in request.files:
        flash("No Image selected", "warning")
        return redirect(url_for('images.upload'))
    else:
        file = request.files['image']
        bucket_name = "nextagram-aws-bucket"
        s3.upload_fileobj(
            file,
            bucket_name,
            file.filename,
            ExtraArgs={
                "ACL": "public-read",
                "ContentType": file.content_type
            }
        )
        image = Image(user = user, image_url = f"https://{bucket_name}.s3-ap-southeast-1.amazonaws.com/{file.filename}")
        if image.save():
            flash("Image Uploaded Successfully", "success")
            return redirect(url_for('users.profile'))
        else:
            flash("Something Went Wrong.", 'danger')
            return render_template("images/new.html")

@images_blueprint.route('/display/<user_id>/<id>')
def display(user_id, id):
    user = User.get_by_id(user_id)
    image = Image.get_by_id(id)
    return render_template('images/display.html', image=image, user=user)