from flask import Flask, jsonify, request
from marshmallow import ValidationError

from application.models import User, Banana
from application.schemas import banana_schema, bananas_schema


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

    @app.route("/banana/<id>", methods=["GET", "PATCH", "DELETE"])
    def banana(id):
        if request.method == 'GET':
            banana = Banana.query.get_or_404(id)
            response = banana_schema.dump(banana)
            return response

        elif request.method == 'PATCH':
            banana = Banana.query.filter(Banana.id == id).one_or_none()
            body = request.get_json()
            if not body:
                response = {"Message": "No input data provided"}
                return response, 400
            if banana:
                try:
                    data = banana_schema.load(body, partial=('color',))
                except ValidationError as e:
                    return e.messages, 422
            else:
                response = {"Message": f"Not found banana with id: {id}"}
                return response, 404

            Banana.query.filter(Banana.id == id).update(body)
            db.session.commit()
            return banana_schema.dump(banana), 200

        elif request.method == 'DELETE':
            banana = Banana.query.filter(Banana.id == id).one_or_none()
            if banana:
                db.session.delete(banana)
                db.session.commit()
                response = {"Message": "Successfully deleted banana"}
                return response, 204
            else:
                response = {
                    "Message": f"Not found banana with id: {id}"
                }
                return response, 404

    @app.route("/banana", methods=["GET", "POST"])
    def handle_banana():
        if request.method == 'GET':
            bananas = Banana.query.all()
            response = jsonify(bananas_schema.dump(bananas))
            return response

        if request.method == 'POST':
            body = request.get_json()
            if not body:
                response = {"Message": "No input data provided"}
                return response, 400
            try:
                data = banana_schema.load(body)
            except ValidationError as e:
                return e.messages, 422
            color = body['color']
            origins = body['origins']
            banana = Banana(color=color, origins=origins)
            db.session.add(banana)
            db.session.commit()
            response = banana_schema.dump(Banana.query.get(banana.id))
            return response, 201
    return app
