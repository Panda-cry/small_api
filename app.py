import os

from dotenv import load_dotenv
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_smorest import Api
from flask_migrate import Migrate
from routes import blp

#Ovo je genijalno jer ga korisitmo kasnije za testiranje ili akoo negde zatreba rad neki sa app
# da imamo app context !!! a moze i iz current app da se cupa ali treba ja mislim da radi app onda !
def create_app():
    load_dotenv()

    app = Flask(__name__)

    app.config["PROPAGETE_EXCEPTIONS"] = os.getenv('PROPAGETE_EXCEPTIONS')
    app.config["API_TITLE"] = os.getenv("API_TITLE")
    app.config["API_VERSION"] = os.getenv("API_VERSION")
    app.config["OPENAPI_VERSION"] = os.getenv("OPENAPI_VERSION")
    app.config["OPENAPI_URL_PREFIX"] = os.getenv("OPENAPI_URL_PREFIX")
    app.config["OPENAPI_SWAGGER_UI_PATH"] = os.getenv(
        "OPENAPI_SWAGGER_UI_PATH")
    app.config[
        "OPENAPI_SWAGGER_UI_URL"] = os.getenv("OPENAPI_SWAGGER_UI_URL")
    app.config[
        "SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")
    app.config[
        'SQLALCHEMY_TRACK_MODIFICATIONS'] = os.getenv(
        "SQLALCHEMY_TRACK_MODIFICATIONS")  # Ovo se često postavlja na False da bi se izbegli upozorenja
    app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY")
    app.config['AUTHLIB_INSECURE_TRANSPORT'] = os.getenv(
        "AUTHLIB_INSECURE_TRANSPORT")
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000
    app.config['SECRET_KEY'] = "this is my secret"

    jwt = JWTManager(app)
    api = Api(app)
    from database import db
    db.init_app(app)
    migrate = Migrate(app,db)
    with app.app_context():
        from models.userModel import User,Sample,Category,Supplie,Magacin,Order,OrderItem,Status
        db.create_all()

    api.spec.components.security_scheme("bearerAuth", {
        "type": "http",
        "scheme": "bearer",
        "bearerFormat": "JWT"
    })

    api.register_blueprint(blp)

    return app


# Super caka mozemo da imamo current_app da kreiramo nove stvari
# mozemo da prenosimo ovaj app sto pravimo!!!

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=5000,
            ssl_context=("localhost.crt", "localhost.key"))
