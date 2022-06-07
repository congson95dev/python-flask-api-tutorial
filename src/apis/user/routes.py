from flask import jsonify, request
from werkzeug.security import generate_password_hash
from flask_restx import Resource, Namespace
from flask_jwt import jwt_required
from src.models.user import db
from src.models.user import User
from src import api
from sqlalchemy import and_, or_, not_

# this have to import below the api variable, because api variable is called in this UserSchema file
from src.schemas.User.UserSchema import user_register_schema
from src.schemas.User.UserSchema import user_update_schema


# we use flask_restx to handle api instead of Flask itself
# in this flask_restx, the function is named by the HTTP method, such as get() = GET, post() = POST
# also, it will show api detail in browser, so we don't need to use postman to test API
# we can test API directly on browser

# add namespace for api, when we run in browser, we will see this in the title of each api block
user_api = Namespace('User', description='User related operations', )
# assign namespace to url prefix
# with this, we will have url prefix = /user
api.add_namespace(user_api, path='/user')


# when we add prefix to api and assign it to namespace, it will now used as a new api
# so you have to use it like @user_api.route, but not @api.route as normal


@user_api.route('/')
class Users(Resource):
    # @jwt_required used to make user must set token before call api
    @jwt_required()
    def get(self):
        search_params = request.args.get('search')
        search = "%{}%".format(search_params)
        users = User.query.filter(
            or_(
                User.username.like(search),
                User.email.like(search)
            )
        ).all()
        result = []
        for user in users:
            user_data = {}
            user_data['email'] = user.email
            user_data['username'] = user.username
            user_data['password'] = user.password

            result.append(user_data)
        if not result:
            return jsonify({'message': 'we cant find any user that matched your request'})
        return jsonify({'users': result})

    # this expect is called to schema, and this schema is like a validate to this function
    # also, it will allow us to edit the value of api in browser
    @user_api.expect(user_register_schema, validate=True)
    def post(self):
        data = request.get_json()
        try:
            user = User(data.get('email'), data.get('username'), data.get('password'))
            db.session.add(user)
            db.session.commit()
        except:
            return jsonify({'message': 'An Exception Occurred'})
        return jsonify({'message': 'User created', 'user_id': user.id})


@user_api.route('/<int:user_id>')
class UserDetail(Resource):
    # @jwt_required used to make user must set token before call api
    @jwt_required()
    def get(self, user_id):
        user = User.query.filter_by(id=user_id).first()
        if not user:
            return jsonify({'message': 'user with id %s does not exist' % user_id})
        result = {
            'id': user.id,
            'email': user.email,
            'username': user.username,
            'password': user.password
        }
        return jsonify({'user': result})

    # @jwt_required used to make user must set token before call api
    @jwt_required()
    # this expect is called to schema, and this schema is like a validate to this function
    # also, it will allow us to edit the value of api in browser
    @user_api.expect(user_update_schema, validate=True)
    def put(self, user_id):
        if user_id:
            user = User.query.filter_by(id=user_id).first()
            if not user:
                return jsonify({'message': 'user with id %s does not exist' % user_id})
            try:
                data = request.get_json()
                if data.get('password'):
                    user.password = data.get('password')
                db.session.commit()
            except:
                return jsonify({'message': 'An Exception Occurred'})
            return jsonify({'message': "User %s's password updated, new password: %s" % (user.username, data.get('password'))})

    # @jwt_required used to make user must set token before call api
    @jwt_required()
    def delete(self, user_id):
        if user_id:
            user = User.query.filter_by(id=user_id).first()
            if not user:
                return jsonify({'message': 'user with id %s does not exist' % user_id})
            try:
                db.session.delete(user)
                db.session.commit()
            except:
                return jsonify({'message': 'An Exception Occurred'})
            return jsonify({'message': 'User deleted'})
