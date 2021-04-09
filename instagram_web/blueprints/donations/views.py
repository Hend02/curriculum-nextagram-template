from flask import Blueprint, render_template, redirect, request, session, flash, url_for
from flask_login import login_user, login_required, current_user
from models.image import Image
from models.user import User
from models.donation import Donation
from helpers import gateway
import requests
import os

donations_blueprint = Blueprint('donations',
                                __name__,
                                template_folder='templates')

@donations_blueprint.route('/<user_id>/<image_id>', methods=['GET'])
@login_required
def new(user_id, image_id):
    user = User.get_by_id(user_id)
    image = Image.get_by_id(image_id)
    client_token = gateway.client_token.generate()
    return render_template('donations/new.html', token=client_token, user=user, image=image)

@donations_blueprint.route('/donate/<user_id>/<image_id>', methods=['POST'])
@login_required
def donate(user_id, image_id):
    result = gateway.transaction.sale({
		"amount": request.form.get('amount'),
		"payment_method_nonce": request.form["nonce"],
		"options": {
			"submit_for_settlement": True
		}
	})
    image = Image.get_by_id(image_id)
    user = User.get_by_id(user_id)
    c_user = User.get_by_id(current_user.id)
    amount = request.form.get('amount')
    print(result.is_success)  
    if result.is_success:
        donation = Donation(image=image, user=c_user, amount=amount)
        donation.save()
        # requests.post(
        #     "https://api.mailgun.net/v3/sandboxa33382b0b48843b3bdf6dd0554343709.mailgun.org/messages",
        #     auth=("api", os.environ.get("MAILGUN_PRIVATE_KEY")),
        #     data={"from": "Mailgun Sandbox postmaster@sandboxa33382b0b48843b3bdf6dd0554343709.mailgun.org",
        #         "to": ["hendrickho1999@yahoo.com"],              
        #         "subject": "Hello Hendrick Ho",
        #         "text": "Congratulations Hendrick Ho, you just sent an email with Mailgun!  You are truly awesome!"
        #     }
        # )
        flash("Donation was Successful. Thank you for your generosity.", 'success')
        return redirect(url_for('users.profile'))
    else:
        client_token = gateway.client_token.generate()
        flash("Something went Wrong. Donation was Unsuccessful.", 'warning')
        return render_template('donations/new.html', token=client_token, user=user, image=image)

