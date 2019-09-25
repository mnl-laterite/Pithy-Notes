from flask import Flask
from flask_restful import Api
from flask_login import LoginManager
from resources.auth import Register, Login, Logout, User, users
from resources.main import Home, Notes, Note
import os

app = Flask(__name__, template_folder='resources/templates', static_folder='resources/static')
key = os.urandom(16)
app.secret_key = key

api = Api(app)
login_manager = LoginManager(app)
login_manager.login_view = '/login'
login_manager.session_protection = "strong"


@login_manager.user_loader
def load_user(username):
    u = users.find_one({"Username": username})
    if not u:
        return None
    return User(u['Username'])


api.add_resource(Home, '/', '/home', '/index')
api.add_resource(Register, '/signup')
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')
api.add_resource(Notes, '/notes')
api.add_resource(Note, '/notes/<string:note_id>')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
