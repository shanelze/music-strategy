from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user


detector_page = Blueprint ('detector_page', __name__, template_folder='/templates')

@detector_page.route ('/detector', methods = ['GET'])
@login_required
def detector ():
    return render_template ("detector.html", user=current_user)

@detector_page.route ('/detector/result', methods=['GET', 'POST'])
@login_required
def detector_result (): 
    # import packages
    from website.models import Scams, db
    from website.pages.gemini_functions import summarise

    # current user id
    user_id = current_user.id

    data_received = {}    

    if request.method == 'POST':
        # import packages
        import speech_recognition as sr
        from website.pages.scam_detection import vectorizer_predict, texblob_predict, gemini_predict

        # receiving data
        text_data = request.form.get('text_data')
        speech_data = request.form.get ('speech_data')
        audio_data = request.files ['audio_data']    

        # checking if data is valid
        if text_data == "" and audio_data.filename == "" and speech_data == "":
            flash ('Please provide either speech, text or audio data.', category='error')
            return redirect (url_for('detector_page.detector'))       

        # append data to dictionary and add to db
        if text_data != "":
            # data summary
            summary = summarise (text_data)

            # add to db
            data = Scams (content=text_data, type="Text", user_id=user_id, summary=summary)
            db.session.add(data) 
            db.session.commit()

            data_received ["Text"] = text_data
        
        if audio_data.filename != "":
            # convert audio to text
            recognizer = sr.Recognizer()
            audioFile = sr.AudioFile (audio_data)
            with audioFile as source:
                data = recognizer.record(source)
            audio_data = recognizer.recognize_google (data, key=None)

            # data summary
            summary = summarise (audio_data)

            # add data tp db
            data = Scams (content=audio_data, type="Audio", user_id=user_id, summary=summary)
            db.session.add(data) 
            db.session.commit()

            data_received ["Audio"] = audio_data
        
        if speech_data != "":
            # data summary
            summary = summarise (speech_data)

            # add data to db
            data = Scams (content=speech_data, type="Speech", user_id=user_id, summary=summary)
            db.session.add(data) 
            db.session.commit()

            data_received ["Speech"] = speech_data
        
    # analysing data using textblob
    analysis_data = texblob_predict(data_received)
        
    # Spam Detection (using the trained model)
    spam_results = vectorizer_predict (data_received)
    # scam detection using gemini
    gemini_results = gemini_predict (data_received)

    # Render the results in detector_result.html
    return render_template("detector_result.html", user=current_user,
                           data_received=data_received,
                           analysis_data=analysis_data,
                           spam_results=spam_results,
                           gemini_results=gemini_results)