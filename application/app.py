from flask import Flask, jsonify

from application.models import User


def create_app(config_name):
    app = Flask(__name__)

    config_module = f"application.config.{config_name.capitalize()}Config"

    app.config.from_object(config_module)

    from application.models import db, migrate

    db.init_app(app)
    migrate.init_app(app, db)

    from application.schemas import ma
    ma.init_app(app)

    @app.route('/')
    def hello_world():
        response = "Hello, World!"
        return jsonify(response)

    @app.route("/users")
    def users():
        num_users = User.query.count()
        response = {
            "Number of users": num_users
        }
        return jsonify(response)

    return app
