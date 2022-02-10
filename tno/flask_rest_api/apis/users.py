from flask_smorest import Blueprint
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from marshmallow import Schema, fields
from marshmallow_sqlalchemy import SQLAlchemySchema

from tno.flask_rest_api import db
from flask.views import MethodView
from tno.shared.log import get_logger
from tno.flask_rest_api.dbmodels import User

logger = get_logger(__name__)

api = Blueprint("users", "users", url_prefix="/users")


class UserSchema(SQLAlchemySchema):
    class Meta:
        model = User
        load_instance: True

    id = auto_field()
    name = auto_field()


class UserListSchema(Schema):
    users = fields.Nested(UserSchema, many=True)


@api.route("/")
class Users(MethodView):
    @api.response(200, UserListSchema)
    def get(self):
        users = db.session.query(User).all()
        return dict(users=users)
