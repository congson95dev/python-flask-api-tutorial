from marshmallow import Schema, fields, pre_dump


# This file purpose is set response by general format
# {
#       "data": ...
#       "message": ...
#       "success": ...
# }


# used in routes
class Responses:
    @staticmethod
    def ok_response(data):
        return {"data": data, "message": "success", "success": True}

    @staticmethod
    def ok_response_without_data():
        return {"message": "success", "success": True}

    @staticmethod
    def not_ok_response(message):
        return {"data": None, "message": message, "success": False}


# used in schemas
class BaseResponseSchema(Schema):
    success = fields.Boolean(default=True)
    message = fields.String()

    @pre_dump
    def preprocess(self, in_data, **kwargs):
        out_data = {
            "data": in_data["data"],
            "success": in_data["success"],
            "message": in_data["message"],
        }
        return out_data
