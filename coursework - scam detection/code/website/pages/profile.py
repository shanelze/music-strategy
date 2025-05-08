from flask import Blueprint, render_template
from flask_login import login_required, current_user
from website.models import Scams

profile_page = Blueprint ('profile_page', __name__, template_folder='/templates')

@profile_page.route ('/profile', methods = ['GET'])
@login_required
def profile ():
    user_id = current_user.id
    scams = Scams.query.filter_by (user_id=user_id).count ()

    # log data
    scam_data = Scams.query.filter_by (user_id=user_id).all ()


    #  speech files
    speech_count = Scams.query.filter_by (type="Speech", user_id=user_id).count ()

    # text files 
    text_count = Scams.query.filter_by (type="Text", user_id=user_id).count ()

    # audio files 
    audio_count = Scams.query.filter_by (type="Audio", user_id=user_id).count ()
    
    return render_template ("profile.html", 
                            user=current_user,
                            scams=scams,
                            scam_data=scam_data,
                            speech_count=speech_count,
                            text_count=text_count, 
                            audio_count=audio_count)