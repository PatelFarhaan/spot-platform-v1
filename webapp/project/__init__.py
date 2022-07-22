# <==================================================================================================>
#                                         IMPORTS
# <==================================================================================================>
from datetime import timedelta

from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_login import LoginManager
from flask_marshmallow import Marshmallow
from flask_mongoengine import MongoEngine
from itsdangerous import URLSafeTimedSerializer

# <==================================================================================================>
#                                         CONFIG
# <==================================================================================================>
# TODO: GET CONFIG FROM A CONFIG FILE

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = "changemePlease"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=3)
app.config['SECRET_KEY'] = "JKjEPw#ytuJP!pbKgN$B!X4F2c5!kDLh"
serial = URLSafeTimedSerializer("JKjEPw#ytuJP!pbKgN$B!X4F2c5!kDLh")
app.config['MONGODB_SETTINGS'] = {'host': "mongodb://admin:admin@localhost/admin"}

CORS(app)
db = MongoEngine(app)
ma = Marshmallow(app)
jwt = JWTManager(app)

login_manager = LoginManager(app)
login_manager.blueprint_login_views = {
    "auth": "auth.login"
}

# <==================================================================================================>
#                                         BLUEPRINT
# <==================================================================================================>
from project.auth.apis import auth_blueprint
from project.error.error_handler import errorpage_blueprint

app.register_blueprint(auth_blueprint)
app.register_blueprint(errorpage_blueprint)
