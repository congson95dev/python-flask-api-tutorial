from marshmallow import ValidationError
from marshmallow.validate import Validator


# set model_name and query
class CustomDBValidator(Validator):
    def __call__(self, *args, **kwargs):
        model_name = args[0]
        self.validator_model = kwargs.pop("validator_model", ValidationError)
        self.model_name = model_name
        self.query = model_name.query
        return kwargs


# filter ignore records which have deleted_by
class CustomDBValidateWithNoneDeleted(CustomDBValidator):
    def __call__(self, *args, **kwargs):
        kwargs = super().__call__(*args, **kwargs)
        self.query = self.model_name.query

        if getattr(self.model_name, "deleted_by", None):
            self.query = self.query.filter_by(deleted_date=None, deleted_by=None)
        return kwargs


# validate check by id to see if records exists in db
class ValidateObjectExistByID(CustomDBValidateWithNoneDeleted):
    def __call__(self, model_name, **kwargs):
        kwargs = super().__call__(model_name, **kwargs)

        self.query = self.query.filter_by(id=kwargs.get("id"))
        data = self.query.first()
        if not data:
            raise self.validator_model(
                "{} {}".format(kwargs.get("name", ""), "not exists")
            )
        return data
