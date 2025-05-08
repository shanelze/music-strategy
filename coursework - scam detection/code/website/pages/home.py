from flask import Blueprint, render_template
from flask_login import login_required, current_user
import requests
from website.models import Scams
import random

home_page = Blueprint ('home_page', __name__, template_folder='/templates')

@home_page.route ('/', methods = ['GET'])
@login_required
def home ():
    # newspage
    from dotenv import load_dotenv
    from pathlib import Path
    import os

    env_path = Path('.')/'.env'
    load_dotenv (dotenv_path=env_path)
    api_key = os.environ.get('NEWS_API_KEY')

    url = f"https://newsapi.org/v2/everything?q=scam&apiKey={api_key}"
    response = requests.get (url)

    count = 0
    article_title = []
    article_description = []
    article_url = []
    img_url = []

    data = response.json ()
    for key, value in data.items ():
        if key == "articles":
            for article in value:
                if article ["title"] != "[Removed]" and article["url"] != "None" and article["urlToImage"] != None and len (article["description"]) > 200:
                    article_title.append (article ["title"])
                    article_description.append (article ["description"])
                    article_url.append (article ["url"])
                    img_url.append (article ["urlToImage"])
                    
                    count += 1 

                    if count == 20:
                        break

    # number of scams prevented
    user_id = current_user.id
    scams = Scams.query.filter_by (user_id=user_id).count ()

    # picking random numbers
    rand_num = random.sample (range(20),3)

    return render_template ("home.html", user=current_user, title=article_title, description=article_description, url=article_url, img=img_url, scams=scams, rand_num=rand_num)