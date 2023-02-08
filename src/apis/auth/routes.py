from datetime import datetime, timezone

from flask import jsonify
from flask import request
from flask_jwt_extended import create_access_token, get_jwt_identity, create_refresh_token
from flask_jwt_extended import current_user
from flask_jwt_extended import get_jwt, get_jti
from flask_jwt_extended import jwt_required
from flask_restx import Resource, Namespace

from src import db
from src import jwt
from src.Config import Config
from src.common.security import authenticate
from src.models import TokenBlocklist
from src.models.user import User

# add namespace for api, when we run in browser, we will see this in the title of each api block
api = Namespace('Auth', description='Auth related operations', )


# this is a trigger called whenever you call function which have jwt_required()
# it will automatic reload variable current_user for you
# we will use variable current_user in class Protected
# docs: https://flask-jwt-extended.readthedocs.io/en/stable/automatic_user_loading/
@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(id=identity).one_or_none()


# this is a trigger called whenever you call function which have jwt_required()
# it will check if the token is revoked or not
# if true, it will throw err, else, it will allow user to access to the api
# docs: https://flask-jwt-extended.readthedocs.io/en/stable/blocklist_and_token_revoking/
@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload: dict) -> bool:
    jti = jwt_payload["jti"]
    token = db.session.query(TokenBlocklist.id).filter_by(jti=jti).scalar()

    return token is not None


@api.route("/login")
class Login(Resource):
    def post(self):
        username = request.json.get("username", None)
        password = request.json.get("password", None)

        user = authenticate(username, password) or None
        if user is None:
            return {
                       "message": "Wrong email or password",
                   }, 401

        # add additional info, such as aud
        additional_claims = {"aud": request.host, "foo": "bar"}

        # create refresh token
        refresh_token = create_refresh_token(identity=user.id, additional_claims=additional_claims)

        # add refresh token to additional_claims
        # so we can use it later in the revoke part in logout action
        additional_claims['refresh_token'] = refresh_token

        # create access token
        access_token = create_access_token(identity=user.id, additional_claims=additional_claims)

        return jsonify(access_token=access_token, refresh_token=refresh_token)


# refresh token
# need to transfer Authorization = Bearer $refresh_token which get from api /login
# FE will check if access token is going to expire soon or not
# if it's true, FE team gonna call this api
# this api will create access token again and return that token to FE,
# so they will copy this new access token and add to other API
# docs: https://flask-jwt-extended.readthedocs.io/en/stable/refreshing_tokens/
@api.route("/refresh")
class Refresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        identity = get_jwt_identity()

        # get claims
        claims = get_jwt()

        # extract from claims to additional_claims
        additional_claims_keys = ['aud', 'foo']
        additional_claims = {x: claims[x] for x in additional_claims_keys}

        # add refresh token from header to additional_claims
        refresh_token = request.headers.environ.get('HTTP_AUTHORIZATION').replace('Bearer ', '')
        additional_claims['refresh_token'] = refresh_token

        # create access token
        access_token = create_access_token(identity=identity, additional_claims=additional_claims)
        return jsonify(access_token=access_token)


@api.route('/protected')
class Protected(Resource):
    # @jwt_required used to make user must set token before call api
    @jwt_required()
    def post(self):
        # use get_jwt() to get additional_claims that we transfer when login
        claims = get_jwt()

        allowed_auds = (
            Config.ALLOWED_AUDS
            if Config.ALLOWED_AUDS
            else []
        )

        # check if url is valid
        if "aud" in claims:
            if claims["aud"] in allowed_auds:
                # we can use current_user whenever we want,
                # just need to add jwt_required and import current_user and add function user_lookup_callback,
                # and then, it's free to use
                # docs: https://flask-jwt-extended.readthedocs.io/en/stable/automatic_user_loading/
                return {
                           "id": current_user.id,
                           "email": current_user.email,
                           "username": current_user.username,
                           "aud": claims['aud']
                       }, 200

        return {
                   "message": f"This url '{claims['aud']}' is not allowed",
               }, 401


# in this logout action, we will try to revoke the access token and refresh token
# so user can't use access token to access to other api, also they can't use refresh token to create new access token
# docs: https://flask-jwt-extended.readthedocs.io/en/stable/blocklist_and_token_revoking/
@api.route("/logout")
class Logout(Resource):
    @jwt_required(verify_type=False)
    def post(self):
        now = datetime.now(timezone.utc)

        # revoke access token by adding the token information to table token_block_list
        # then we will use token_block_list to check revoked token in function check_if_token_revoked
        token = get_jwt()
        jti = token["jti"]
        ttype = token["type"]
        db.session.add(TokenBlocklist(jti=jti, type=ttype, created_at=now))

        # revoke refresh token by adding the token information to table token_block_list
        # then we will use token_block_list to check revoked token in function check_if_token_revoked
        refresh_token = token["refresh_token"]
        jti_refresh_token = get_jti(refresh_token)
        ttype = "refresh"
        db.session.add(TokenBlocklist(jti=jti_refresh_token, type=ttype, created_at=now))

        # commit
        db.session.commit()

        return {
                   "message": "Logout successfully",
               }, 200