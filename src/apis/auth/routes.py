from flask_restx import Resource, Namespace
from flask_jwt import jwt_required, current_identity
from src import api

# add namespace for api, when we run in browser, we will see this in the title of each api block
auth_api = Namespace('Auth', description='Auth related operations', )
# assign namespace to url prefix
# with this, we will have url prefix = /auth
api.add_namespace(auth_api, path='/auth')


@auth_api.route('/protected')
class Protected(Resource):
    # @jwt_required used to make user must set token before call api
    @jwt_required()
    def post(self):
        return '%s' % current_identity
