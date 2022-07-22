# # <==================================================================================================>
# #                                       IMPORTS
# # <==================================================================================================>
# from common_utilities.jwt_decoder import user_jwt_decoder
# from flask import url_for, request, jsonify, redirect, session, render_template
# from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
# from flask_login import login_required, login_user
# from project import serial
# from project.models import Users
# from project.auth.json_schema_validation.user_schema_validation import validate_login_schema, validate_email_schema, \
#     validate_delete_acc_schema, validate_register_schema
# from project.auth.serializer.marshmallow_serialize import UserSchema
# from werkzeug.security import generate_password_hash, check_password_hash
#

# # <==================================================================================================>
# #                                  IS JWT TOKEN EXPIRED CHECK
# # <==================================================================================================>
# @user_blueprint.route('/jwt-token-check', methods=["GET"])
# @jwt_required()
# def expired_jwt_token_check():
#     resp_obj = {
#         "result": True,
#         "message": "token is valid"
#     }
#     return jsonify(resp_obj)
#
#
# # <==================================================================================================>
# #                                      PASSWORD RESET LINK
# # <==================================================================================================>
# @user_blueprint.route('/reset-link/<token>', methods=['GET', 'POST'])
# def reset_link(token):
#     if request.method == "GET":
#         return render_template("reset.html")
#
#     elif request.method == "POST":
#         try:
#             email = serial.loads(token, salt='email_reset', max_age=int(CONSTANT.PASSWORD_RESET_LINK_AGE.value))
#             print(f"auth: reset-link/token: reset password link clicked: {email}")
#             if email:
#                 user_obj = Users.objects.filter(email=email).first()
#                 user_obj.is_logged_in = False
#                 user_obj.save()
#                 print(f"auth: reset-link/token: user logged out: {email}")
#                 email = email.lower()
#         except:
#             return redirect(f"{CONSTANT.CURRENT_SERVER.value}", code=302)
#
#         user = Users.objects.filter(email=email).first()
#         if user:
#             password = request.form.get("password")
#
#             if user.password_reset_meta_data == {}:
#                 return redirect(f"{CONSTANT.CURRENT_SERVER.value}", code=302)
#
#             if not user.password_reset_meta_data["is_clicked"]:
#                 user.password = generate_password_hash(password)
#                 user.password_reset_meta_data = {}
#                 user.save()
#                 print(f"auth: reset-link/token: password changed: {email}")
#                 return render_template("reset-success-inv.html")
#         else:
#             print(f"auth: reset-link/token: user does not exist: {email}")
#             return redirect(f"{CONSTANT.CURRENT_SERVER.value}", code=302)
#
#
# # <==================================================================================================>
# #                               PASSWORD RESET REQUEST (HOMEPAGE)
# # <==================================================================================================>
# @user_blueprint.route('/forgot-password', methods=['POST'])
# def forgot_password():
#     input_request = request.get_json()
#     response = validate_email_schema(input_request)
#     if response["result"]:
#         email = response["data"]["email"]
#         if email:
#             email = email.lower()
#         user = Users.objects.filter(email=email).first()
#
#         if user is None:
#             print(f"auth: forgot-password: user does not exist : {email}")
#             return jsonify({"result": True, "message": "email sent if the user exists"})
#
#         token = serial.dumps(user.email, salt='email_reset')
#         link = url_for('auth.reset_link', token=token, _external=True)
#         user.password_reset_meta_data = {"is_clicked": False}
#         user.save()
#         print(f"auth: forgot-password: forgot password link generated: {email}")
#
#         return jsonify({"result": True, "message": "email sent if the user exists"})
#     else:
#         return jsonify(response)
#
#
# # <==================================================================================================>
# #                                   EMAIL CONFIRMATION TOKEN
# # <==================================================================================================>
# @user_blueprint.route('/email-confirmed/<token>', methods=['GET'])
# def email_confirmed(token):
#     try:
#         email = serial.loads(token, salt='email_confirm')
#         print(f"auth: email-confirmed: email confirmation link clicked: {email}")
#         if email:
#             email = email.lower()
#     except:
#         return redirect(f"{CONSTANT.CURRENT_SERVER.value}/login", code=302)
#
#     user = Users.objects.filter(email=email).first()
#
#     if user:
#         if user.passowrd_confirm_meta_data == {}:
#             return redirect(f"{CONSTANT.CURRENT_SERVER.value}/login", code=302)
#         else:
#             user.email_confirmed = True
#             user.save()
#             print(f"auth: email-confirmed: email confirmed: {email}")
#
#         login_user(user)
#         user.is_logged_in = True
#         user.passowrd_confirm_meta_data = {}
#         user.save()
#         session["email"] = email
#
#         print(f"auth: email-confirmed: logged in: {email}")
#         return redirect(url_for("auth.confirmation_signup_flow", email=email, code=302))
#
#     else:
#         print(f"auth: email-confirmed: user does not exist {email}")
#         return redirect(f"{CONSTANT.CURRENT_SERVER.value}/auth/signup")
#
#
# # <==================================================================================================>
# #                                   CONFIRMATION SIGNUP FLOW
# # <==================================================================================================>
# @user_blueprint.route('/confirmation-signup-flow', methods=["GET"])
# @login_required
# def confirmation_signup_flow():
#     email = session.get("email")
#
#     if email:
#         email = email.lower()
#
#     if not email:
#         print(f"auth: confirmation-signup-flow: email not in session: {email}")
#         return jsonify({"reuslt": False, "error": "session expired"})
#
#     inv_obj = Users.objects.filter(email=email).first()
#     first_name = (inv_obj.first_name).strip().replace(" ", "_")
#     last_name = (inv_obj.last_name).strip().replace(" ", "_")
#     query_string = f"confirmed=True&email={inv_obj.email}&fn={first_name}&ln={last_name}&auth=true"
#     print(f"auth: confirmation-signup-flow: redirect to onboarding flow: {email}")
#     return redirect(f"{CONSTANT.CURRENT_SERVER.value}/auth/signup?{query_string}"), 302
#
#

#
#

#
#
# # <==================================================================================================>
# #                                      UPDATE INFORMATION
# # <==================================================================================================>
# @user_blueprint.route('/update-info', methods=['PATCH'])
# @jwt_required()
# def update_info():
#     jwt_decode = user_jwt_decoder(get_jwt_identity())
#     if not jwt_decode["result"]:
#         return jsonify(jwt_decode)
#
#     user_obj = jwt_decode["user_obj"]
#
#     if user_obj.is_logged_in:
#         input_data = request.get_json()
#         available_fields = {"sectors", "deals", "bio", "location", "prior_investments", "first_invite",
#                             "accreditation", "syndicate", "angel", "profile_pic_link", "first_dashboard_visit"}
#
#         for key in list(input_data.keys()):
#             if key not in available_fields:
#                 print(f"auth: update-info: {key} key does not exist in available fields: {user_obj.email}")
#                 return jsonify({"result": False, "error": "invalid user field"})
#
#         ma_schema = UserSchema()
#         user_objs = ma_schema.dump(user_obj)
#
#         ret_obj = {
#             "result": True,
#             "user": user_objs,
#         }
#         return ret_obj
#     else:
#         return jsonify({"result": False, "error": "user is not authenticated"})
#
#
# # <==================================================================================================>
# #                               CHANGE PASSWORD (PROFILE SETTINGS)
# # <==================================================================================================>
# @user_blueprint.route('/change-password', methods=["GET"])
# @jwt_required()
# def change_password():
#     jwt_decode = user_jwt_decoder(get_jwt_identity())
#     if not jwt_decode["result"]:
#         return jsonify(jwt_decode)
#
#     inv_obj = jwt_decode["user_obj"]
#
#     if inv_obj is not None:
#         token = serial.dumps(inv_obj.email, salt='email_reset')
#         link = url_for('auth.reset_link', token=token, _external=True)
#         inv_obj.password_reset_meta_data = {"is_clicked": False}
#         inv_obj.save()
#         print(f"auth: change-password: password link generated: {inv_obj.email}")
#         return jsonify({"result": True, "message": "email sent if the user exists"})
#     else:
#         return jsonify({"result": False, "error": "user does not exists"})
#
#
# # <==================================================================================================>
# #                                    VERIFY PASSOWRD :=> DELETE ACCOUNT
# # <==================================================================================================>
# @user_blueprint.route('/verify-password', methods=["POST"])
# @jwt_required()
# def verify_password():
#     jwt_decode = user_jwt_decoder(get_jwt_identity())
#     if not jwt_decode["result"]:
#         return jsonify(jwt_decode)
#
#     inv_obj = jwt_decode["user_obj"]
#
#     response = validate_delete_acc_schema(request.get_json())
#     if response["result"]:
#         password = response["data"]["password"]
#         if check_password_hash(inv_obj.password, password):
#             print(f"auth: verify-password: correct password: {inv_obj.email}")
#             return jsonify({"result": True, "message": "correct credentials"})
#         print(f"auth: verify-password: wrong password: {inv_obj.email}")
#         return jsonify({"result": False, "message": "wrong credentials"})
#     return jsonify(response)
#
#
# # <==================================================================================================>
# #                                  GET JWT TOKEN FOR CONFIRMATION PAGE
# # <==================================================================================================>
# @user_blueprint.route('/get-jwt-token', methods=['POST'])
# def jwt_for_confirmation_page():
#     input_request = request.get_json()
#     response = validate_email_schema(input_request)
#     if response["result"]:
#         email = response["data"]["email"]
#
#         if email:
#             email = email.lower()
#
#         user = Users.objects.filter(email=email).first()
#         if user is None:
#             error = "user does not exist"
#             print(f"auth: get-jwt-token: {error}: {email}")
#             return jsonify({"result": False, "error": error})
#
#         jwt_obj = {"email": email, "model": "Users"}
#         access_token = create_access_token(identity=jwt_obj)
#         ret_obj = {
#             "result": True,
#             "token": access_token
#         }
#         print(f"auth: get-jwt-token: new jwt token generated: {email}")
#         return jsonify(ret_obj)
#     else:
#         return jsonify(response)
