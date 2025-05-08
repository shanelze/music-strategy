from flask import Blueprint, render_template
from flask_login import login_required, current_user

rewards_page = Blueprint ('rewards_page', __name__, template_folder='/templates')

@rewards_page.route ('/rewards', methods = ['GET'])
@login_required
def rewards ():
    return render_template ("rewards.html", user=current_user)