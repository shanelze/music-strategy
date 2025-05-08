from flask import Blueprint, render_template
from flask_login import login_required, current_user

learning_page = Blueprint ('learning_page', __name__, template_folder='/templates')

@learning_page.route ('/learning', methods = ['GET'])
@login_required
def learning ():
    return render_template ("learning.html", user=current_user)