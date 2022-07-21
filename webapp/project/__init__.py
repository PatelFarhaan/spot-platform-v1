# <==================================================================================================>
#                                         IMPORTS
# <==================================================================================================>
from flask_cors import CORS
from datetime import timedelta
from flask import Flask, session
from flask_login import LoginManager
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from flask_mongoengine import MongoEngine
from itsdangerous import URLSafeTimedSerializer


# <==================================================================================================>
#                                         CONFIG
# <==================================================================================================>
app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = "changemePlease"
app.config['SECRET_KEY'] = "JKjEPw#ytuJP!pbKgN$B!X4F2c5!kDLh"
serial = URLSafeTimedSerializer("JKjEPw#ytuJP!pbKgN$B!X4F2c5!kDLh")
app.config['MONGODB_SETTINGS'] = {'host': "mongodb://admin:admin@localhost/admin"}

CORS(app)
db = MongoEngine(app)
ma = Marshmallow(app)
jwt = JWTManager(app)


@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=60)


login_manager = LoginManager(app)
login_manager.blueprint_login_views = {
    "users": "users.login"
}

# <==================================================================================================>
#                                         BLUEPRINT
# <==================================================================================================>
from project.error.error_handler import errorpage_blueprint
from project.users.views import user_blueprint

app.register_blueprint(errorpage_blueprint)
app.register_blueprint(user_blueprint)
