import jsonschema
import json
import os
from flask import request
from flask_restful import Resource
from flask_login import login_user

from google.oauth2 import id_token
from google.auth.transport import requests
from splash.login import User
from splash.categories.users.users_service import (
    UserService, 
    MultipleUsersAuthenticatorException,
    UserNotFoundException)

# TODO: Create error handling for if the user is not found in the mongo database
# TODO: integrate this with mongo 


class OauthVerificationError(ValueError):
    pass


class UserNotFoundError(Exception):  # TODO: make the base class more specific
    pass


class OAuthResource(Resource):

    def __init__(self, user_service: UserService):
        self.CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID") + ".apps.googleusercontent.com" #TODO: Temporary solution, we will need to have a local config file
        AUTH_SCHEMA = open_schema()
        self.validator = jsonschema.Draft7Validator(AUTH_SCHEMA)
        self.user_service = user_service

    def post(self):
        try:
            payload = request.get_json(force=True)
            self.validator.validate(payload)
            token = payload['token']
            # Specify the CLIENT_ID of the app that accesses the backend:
            idinfo = id_token.verify_oauth2_token(token, requests.Request(), self.CLIENT_ID)

            # Or, if multiple clients access the backend server:
            # idinfo = id_token.verify_oauth2_token(token, requests.Request())
            # if idinfo['aud'] not in [CLIENT_ID_1, CLIENT_ID_2, CLIENT_ID_3]:
            #     raise ValueError('Could not verify audience.')

            if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                raise ValueError('Wrong issuer.')

            # If auth request is from a G Suite domain:
            # if idinfo['hd'] != GSUITE_DOMAIN_NAME:
            #     raise ValueError('Wrong hosted domain.')

            # ID token is valid. Get the user's Google Account ID from the decoded token.
            # user = User("foo", idinfo['email'], idinfo['given_name'], idinfo['family_name'], True) 
            try:
                user_dict = self.user_service.get_user_authenticator(idinfo['iss'], idinfo['sub'])
            except UserNotFoundException:
                # it's possible that we want to not throw an error,
                # so that the client has a chance to le the user register
                raise UserNotFoundError('User not registered')
            user = User(user_dict['uid'], idinfo['email'], idinfo['given_name'], idinfo['family_name'], True)
            login_user(user)
            return {'message': 'LOGIN SUCCESS', 'user': dict(user)}
             
        except ValueError as e:
            # This should catch any ValueErrors that come from the the id_token.verify_oauth2_token
            # However, there are still possible connection errors from that function that may
            # go uncaught
            raise OauthVerificationError(e) from None

        except MultipleUsersAuthenticatorException as e:
            raise OauthVerificationError(e) from None


def open_schema():
    dirname = os.path.dirname(__file__)
    auth_schema_file = open(os.path.join(dirname, "auth_schema.json"))
    AUTH_SCHEMA = json.load(auth_schema_file)
    auth_schema_file.close()
    return AUTH_SCHEMA