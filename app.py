from flask import Flask, jsonify, after_this_request
import models
from resources.posts import posts
from resources.user import user
from resources.comments import comments
from flask_login import LoginManager
import os
from dotenv import load_dotenv
load_dotenv()
from flask_cors import CORS

DEBUG = True
PORT = os.environ.get("PORT")

app = Flask(__name__)

CORS(user, origins=['https://hello-stranger-application.herokuapp.com/','http://localhost:3000'], supports_credentials=True)
CORS(posts, origins=['https://hello-stranger-application.herokuapp.com/','http://localhost:3000'], supports_credentials=True)
CORS(comments,  origins=['https://hello-stranger-application.herokuapp.com/','http://localhost:3000'], supports_credentials=True)

app.secret_key=os.environ.get("APP_SECRET")

app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='None',
)

login_manager = LoginManager()
login_manager.init_app(app)
@login_manager.user_loader
def load_user(userid):
    try:
        return models.User.get(models.User.id == userid)
    except models.DoesNotExist:
        return None


app.register_blueprint(posts, url_prefix='/posts')
app.register_blueprint(comments, url_prefix='/posts')
app.register_blueprint(user, url_prefix='/user')

@app.before_request
def before_request():
    """Connect to the db before each request"""
    print("you should see this before each request")
    models.DATABASE.connect()

    @after_this_request
    def after_request(response):
        """Close the db connection after each request"""
        print("you should see this before each request")
        models.DATABASE.close()
        return response

if os.environ.get('FLASK_ENV') != 'development':
    print('\non heroku!')
    models.initialize()

if __name__ == "__main__":
    models.initialize()
    app.run(debug=DEBUG, port=PORT)