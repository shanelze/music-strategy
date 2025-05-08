from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import markdown

# database initialisation
db = SQLAlchemy ()
DB_NAME = "database.db"

def create_app ():
    app = Flask(__name__)
    app.config ['SECRET_KEY'] = 'BC3415'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    # Define the custom markdown filter
    @app.template_filter('markdown')
    def markdown_filter(text):
        if text:
            return markdown.markdown(text)
        else:
            return ""

    # Register the filter
    app.jinja_env.filters['markdown'] = markdown_filter

    # import views from different apps
    from .auth.start import auth_views
    from .pages.home import home_page
    from .pages.forum import forum_page
    from .pages.rewards import rewards_page
    from .pages.detector import detector_page
    from .pages.learning import learning_page
    from .pages.profile import profile_page
    from .pages.faq import faq_page

    app.register_blueprint (auth_views, url_prefix='/')
    app.register_blueprint (home_page, url_prefix='/')
    app.register_blueprint (forum_page, url_prefix='/')
    app.register_blueprint (rewards_page, url_prefix='/')
    app.register_blueprint (detector_page, url_prefix='/')
    app.register_blueprint (learning_page, url_prefix='/')
    app.register_blueprint (profile_page, url_prefix='/')
    app.register_blueprint (faq_page, url_prefix='/')

    from .models import User

    with app.app_context():
        db.create_all()

    # redirecting the user for when they are not logged in to their account
    login_manager = LoginManager()
    login_manager.login_view = 'auth_views.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user (id):
        return User.query.get (int(id))

    return app
