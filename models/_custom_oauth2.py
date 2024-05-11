import os

from authlib.integrations.flask_client import OAuth


class MyOauth2:

    def __init__(self, current_app):
        self.current_app = current_app

        self.oauth2 = OAuth(self.current_app)

    def register_app(self):
        reg_app = self.oauth2.register(
            "oauth2app",
            client_id=os.getenv("CLIENT_ID_GOOGLE"),
            client_secret=os.getenv("CLIENT_SECRET_GOOGLE"),
            client_kwargs={
                "scope": "openid profile email",
            },
            base_url="https://docs.googleapis.com",
            access_token_url='https://accounts.google.com/o/oauth2/token',
            authorize_url='https://accounts.google.com/o/oauth2/auth',
            jwks_uri='https://www.googleapis.com/oauth2/v3/certs',
        )

        return reg_app
