from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from website.pages.gemini_functions import chatbot_reply
from website.models import FAQ, Chatbot
from website import db
import markdown
import json

faq_page = Blueprint ('faq_page', __name__, template_folder='/templates')
@faq_page.route ('/faq', methods = ['GET'])
@login_required
def faq ():
    # gather previous chat history
    user_id = current_user.id
    faq = FAQ.query.filter_by (user_id=user_id).all()
    chatbot = Chatbot.query.filter_by (user_id=user_id).all()

    # convert text to markdown format
    md_response = {}
    for item in chatbot:
        md_response[item.id] = markdown.markdown(item.chatbot_response)

    return render_template ("faq.html", user=current_user,
                            faq=faq,
                            chatbot=chatbot,
                            md_response=md_response)

@faq_page.route ('/faq/ask', methods = ['POST'])
@login_required
def ask ():
    user = current_user.id
    user_input = request.json.get('question')
    response = chatbot_reply (user_input, user)
    return jsonify({"response": response})

@faq_page.route ('/faq/delete', methods = ['POST'])
@login_required
def delete ():
    user_id = json.loads (request.data) ["userId"]
    if user_id: 
        # delete user chat history
        faq = FAQ.query.filter_by (user_id=user_id).all ()
        for item in faq:
            db.session.delete(item) 
            db.session.commit()

        # delet gemini chat history
        chatbot = Chatbot.query.filter_by (user_id=user_id).all()
        for item in chatbot:
            db.session.delete(item) 
            db.session.commit()

    return jsonify({})