# <==================================================================================================>
#                                      IMPORTS
# <==================================================================================================>
import sys
import jwt
from functools import wraps
from flask import jsonify, request

sys.path.append("../")
from project import app
from project.models import Users


# <==================================================================================================>
#                                      USER JWT DECODER
# <==================================================================================================>
def user_jwt_decoder(encoded_identifier):
    email = encoded_identifier["email"]
    user_obj = Users.objects.filter(email=email).first()

    if not user_obj:
        return {"result": False,
                "error": "user not found"}
    return {
        "result": True,
        "user_obj": user_obj
    }


# <==================================================================================================>
#                                      USER JWT DECODER
# <==================================================================================================>
def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']

        if not token:
            return jsonify({'message': 'a valid token is missing'})
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = Users.query.filter_by(public_id=data['public_id']).first()
        except:
            return jsonify({'message': 'token is invalid'})

        return f(current_user, *args, **kwargs)

    return decorator