from flask import Flask, render_template, request
from flask_migrate import Migrate
from flask_login import LoginManager

from .config import Config
from .models import db, User
from .notes.routes import notes_bp
from .users.routes import users_bp
from .auth.routes import auth_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate = Migrate(app, db)

    app.register_blueprint(notes_bp, url_prefix='/notes')
    app.register_blueprint(users_bp, url_prefix='/users')
    app.register_blueprint(auth_bp, url_prefix='/auth')

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @app.route("/about")
    def about():
        return render_template("about.html", app_name="Notes App")


    @app.route("/contact", methods=['get', 'post'])    
    def contact():
        if request.method == 'GET':
            return render_template("contact.html")
        if request.method == 'POST':
            return "Form sent correctly", 201
        return "Contact page"
    
    return app
