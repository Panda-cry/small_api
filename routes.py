import datetime
from authlib.integrations.flask_client import OAuth
from flask.views import MethodView
from flask_jwt_extended import jwt_required, create_access_token, \
    create_refresh_token
from flask_smorest import Blueprint
from flask import current_app, url_for, redirect, session
from schemas import LoginSchema, JWTtokenSchema
import os
from oauthlib.oauth2 import WebApplicationClient

blp = Blueprint(__name__, "auth", url_prefix="/api", description="AUTH za app")

oauth = OAuth(current_app)
oauth.register(
    "auth0",
    client_id=os.getenv("CLIENT_ID"),
    client_secret=os.getenv("CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'https://{os.getenv("DOMAIN")}/.well-known/openid-configuration'
)

google_client_id = "98243793459-44os5rn3n4gr1gjnp0is8lcsijndnj0f.apps.googleusercontent.com"
google_client_secret = "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"

google_client = WebApplicationClient(google_client_id)


@blp.route("/jwt")
class JWToken(MethodView):

    @blp.arguments(LoginSchema)
    @blp.response(200, JWTtokenSchema)
    def post(self, login_data: LoginSchema):
        if login_data['username'] == "pera123":
            access_token = create_access_token("1", fresh=True,
                                               expires_delta=datetime.timedelta(
                                                   days=10))
            refresh_token = create_refresh_token("1",
                                                 expires_delta=datetime.timedelta(
                                                     seconds=10))
            return {"access_token": access_token,
                    "refresh_token": refresh_token}

    # Da bi dodali jwt u docs moramo ovako da odradimo!!! jer ovde kazemo da docs traze security koji konfig u app
    @jwt_required(fresh=True)
    @blp.doc(security=[{"bearerAuth": []}])
    def get(self):
        print("hahaha")
        return {"message": "This is protected route"}, 200


from models._custom_oauth2 import MyOauth2


@blp.route("/login")
class Login(MethodView):

    def get(self):
        oauth = MyOauth2(current_app)
        oauth2 = oauth.register_app()

        return oauth2.authorize_redirect(
            redirect_uri=url_for("routes.CallMeBack", _external=True)
        )

    def post(self):
        return oauth.auth0.authorize_redirect(
            redirect_uri=url_for("CallMeBack", _external=True)
        )


@blp.route("/home")
class Home(MethodView):
    def get(self):
        print("Peca")
        print(session['user'])
        return session['user']

    def post(self):
        print("Peca")
        return session['user']


@blp.route("/callback")
class CallMeBack(MethodView):

    def get(self):
        oauth = MyOauth2(current_app)
        oauth2 = oauth.register_app()
        token = oauth2.authorize_access_token()

        session["user"] = token
        return redirect("/api/home")

    def post(self):
        token = oauth.auth0.authorize_access_token()

        session["user"] = token
        return redirect("/api/home")


from database import db


@blp.route("/add_test")
class Add_test(MethodView):

    def get(self):
        from models.userModel import Category, Sample, Order, OrderItem, \
            Status, Delivery, User, Supplie
        # cat = Category.query.get(2)
        ord=Order.query.get(1)
        model=Delivery(order=ord,expected_del=datetime.datetime.now())

        db.session.add(model)
        db.session.commit()

        return "Made it"
