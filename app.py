from flask import Flask
import models
from resources.posts import posts
from resources.user import user
from flask_login import LoginManager

DEBUG = True
PORT = 8000

app = Flask(__name__)

app.secret_key="LJAKLJLKJJLJKLSDJLKJASD"
login_manager = LoginManager()

login_manager.init_app(app)
@login_manager.user_loader
def load_user(userid):
    try:
        return models.User.get(models.User.id == userid)
    except models.DoesNotExist:
        return None


app.register_blueprint(posts, url_prefix='/hellostranger/posts')
app.register_blueprint(user, url_prefix='/hellostranger/user')

if __name__ == "__main__":
    models.initialize()
    app.run(debug=DEBUG, port=PORT)