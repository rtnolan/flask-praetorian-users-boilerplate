import os
import pendulum
from flask import Flask, request, jsonify, current_app, url_for
import flask_praetorian

from . import api
from flask_praetorian_users_boilerplate import guard, db, mail
from flask_praetorian_users_boilerplate.models.user import User
from flask_praetorian_users_boilerplate.email import send_email


@api.route('/auth/register', methods=['POST'])
def register():
    """
    Registers a new user by parsing a POST request containing new user info and
    dispatching an email with a registration token
    .. example::
       $ curl http://localhost:5000/api/v1/auth/register -X POST \
         -d '{
           "username":"joebloggs", \
           "password":"password" \
           "email":"test@example.com"
         }'
    """
    logger = current_app.logger
    req = request.get_json(force=True)
    username = req.get('username', None)
    email = req.get('email', None)
    password = req.get('password', None)
    new_user = User(
        username=username,
        password=guard.hash_password(password),
        email=email,
        roles='operator',
    )
    db.session.add(new_user)
    db.session.commit()
    app = current_app._get_current_object()
    # guard.send_registration_email(email, user=new_user,
    #                                     confirmation_sender=app.config['MAIL_USERNAME'],
    #                                     subject='User Registration')
    token = guard.encode_jwt_token(
                new_user,
                override_access_lifespan=pendulum.duration(minutes=15),
                bypass_user_check=True, is_registration_token=True,
            )
    send_email(new_user.email, 'Confirm Your Account',
                   'email/confirm', user=new_user, token=token)
    ret = {'message': 'successfully sent registration email to user {}'.format(
        new_user.username
    )}

    return jsonify(ret)

@api.route('/auth/verify/<token>', methods=['GET'])
def verify(token):
    """
    Finalizes a user registration with the token that they were issued in their
    registration email
    .. example::
       $ curl http://localhost:5000/api/v1/auth/verify -X GET \
         -H "Authorization: Bearer <your_token>"
    """
    logger = current_app.logger
    # registration_token = guard.read_token_from_header()
    # print("TOKEN_: ", registration_token)
    user = guard.get_user_from_registration_token(token)
    # perform 'activation' of user here...like setting 'active' or something
    ret = {'access_token': guard.encode_jwt_token(user)}
    logger.debug("ENCODED NEW TOKEN")
    return jsonify(ret), 200

@api.route('/auth/login', methods=['POST'])
def login():
    """
    Logs a user in by parsing a POST request containing user credentials and
    issuing a JWT token.
    .. example::
       $ curl http://localhost:5000/api/v1/auth/login -X POST \
         -d '{"username":"Walter","password":"calmerthanyouare"}'
    """
    req = request.get_json(force=True)
    username = req.get('username', None)
    password = req.get('password', None)
    user = guard.authenticate(username, password)
    ret = {'access_token': guard.encode_jwt_token(user)}
    return (jsonify(ret), 200)

@api.route('/auth/refresh', methods=['GET'])
def refresh():
    """
    Refreshes an existing JWT by creating a new one that is a copy of the old
    except that it has a refrehsed access expiration.
    .. example::
       $ curl http://localhost:5000/api/v1/auth/refresh -X GET \
         -H "Authorization: Bearer <your_token>"
    """
    old_token = guard.read_token_from_header()
    new_token = guard.refresh_jwt_token(old_token)
    return jsonify(access_token=new_token)
