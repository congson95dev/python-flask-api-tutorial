from src import api
from src.apis.auth.routes import api as auth
from src.apis.user.routes import api as user
from src.apis.book.routes import api as book

# create prefix for API
# with this, we will have url prefix = /auth
# we will do the same with other prefixes
api.add_namespace(auth, path="/auth")
api.add_namespace(user, path="/user")
api.add_namespace(book, path="/book")
