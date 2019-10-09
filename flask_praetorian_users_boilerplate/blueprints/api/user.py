import pendulum
from . import api
from flask_praetorian_users_boilerplate.models.user import User
from flask import Flask, request, jsonify, current_app, url_for
from flask_praetorian_users_boilerplate import guard, db, mail
import flask_praetorian


@api.route('/user/update', methods=['POST'])
@flask_praetorian.auth_required
def update():
    """
    A protected endpoint. The auth_required decorator will require a header
    containing a valid JWT
    .. example::
       $ curl http://localhost:5000/protected -X GET \
         -H "Authorization: Bearer <your_token>"
    """
    req = request.get_json(force=True)
    username = req.get('username', None)
    if not username == flask_praetorian.current_user().username:
        flask_praetorian.current_user().username = username
        db.session.add(flask_praetorian.current_user())
        db.session.commit()
    return jsonify(message='protected endpoint (allowed user {})'.format(
        flask_praetorian.current_user().username,
    ))

@api.route('/ping')
def ping():
    return {'ping': 'pong'}