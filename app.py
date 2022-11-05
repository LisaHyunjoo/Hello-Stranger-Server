from flask import Flask
import models
from resources.posts import posts

DEBUG = True
PORT = 8000

app = Flask(__name__)

app.register_blueprint(posts, url_prefix='/posts')

if __name__ == "__main__":
    models.initialize()
    app.run(debug=DEBUG, port=PORT)