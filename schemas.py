from marshmallow import Schema,fields,validate



class JWTtokenSchema(Schema):
    access_token = fields.String(allow_none=False)
    refresh_token = fields.String(allow_none=False)


class LoginSchema(Schema):
    username = fields.String(validate=validate.Length(5))
    email = fields.Email(validate=validate.Length(10))