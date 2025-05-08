from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
from website.models import Topic, Thread, Comment, GeminiComment
from website import db
from website.pages.gemini_functions import comment_reply

forum_page = Blueprint ('forum_page', __name__, template_folder='/templates')


@forum_page.route ('/forum', methods = ['GET', 'POST'])
@login_required
def topic ():
    # adding new topic to database
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        if title == "" or description == "":
            flash ('Title or description is empty.', category='error')
        else: 
            topic =  Topic(title = title, description = description)
            db.session.add (topic)
            db.session.commit ()

    # retrieve topics
    topics = db.session.execute (db.select(Topic)).scalars ()

    return render_template ("forum_topic.html", user=current_user, topics=topics)

@forum_page.route ('/forum/<title>', methods = ['GET', 'POST'])
@login_required
def thread (title):
    # adding new thread to database
    if request.method == 'POST':
        thread_title = request.form.get('title')
        thread_description = request.form.get('description')
        print (thread_title)
        print (thread_description)

        if thread_title == "" or thread_description == "":
            flash ('Title or description is empty.', category='error')

        else:
            threads = Thread (title = thread_title, description = thread_description, topic_title=title)
            db.session.add (threads)
            db.session.commit ()

    # retrieve comments
    threads = Thread.query.filter_by (topic_title=title).all ()

    # retrieve topic
    topic = Topic.query.get (title)

    return render_template ("forum_thread.html", 
                            user=current_user, 
                            threads=threads, 
                            topic=topic)

@forum_page.route ('/forum/<title>/<int:thread_id>', methods = ['GET', 'POST'])
@login_required
def comment (title, thread_id):
    # adding new topic to database
    if request.method == 'POST':
        
        comment = request.form['comment']
        
        if comment == "":
            flash ('Comment is empty.', category='error')
        else: 
            comment = Comment (comment=comment, thread_id=thread_id)
            db.session.add (comment)
            db.session.commit ()

            # gemini's reply
            response = comment_reply (request.form['comment'], thread_id)

            gemini_comment = GeminiComment (response=response, comment_id=comment.id, thread_id=thread_id)
            db.session.add (gemini_comment)
            db.session.commit ()

    # retrieve topic
    topic = Topic.query.get(title)
    
    # retrieve thread
    thread = Thread.query.get(thread_id)

    # retrieve comments
    comments = Comment.query.filter_by (thread_id=thread_id).all ()

    # retrieve gemini replies
    gemini_replies  = GeminiComment.query.filter_by (thread_id=thread_id).all ()

    return render_template ("forum_comment.html", 
                            user=current_user, 
                            topic=topic, 
                            thread=thread, 
                            comments=comments, 
                            gemini_replies=gemini_replies)