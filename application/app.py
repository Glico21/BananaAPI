from datetime import datetime

from flask import Flask, jsonify, request
from marshmallow import ValidationError

from application.models import User, Banana, Palm
from application.schemas import banana_schema, bananas_schema, palm_schema, palms_schema


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

    @app.route("/palm/<id>", methods=['GET', 'PATCH', 'DELETE'])
    def palm(id):
        if request.method == 'GET':
            palm = Palm.query.get_or_404(id)
            response = palm_schema.dump(palm)
            return response

        elif request.method == 'PATCH':
            palm = Palm.query.filter(Palm.id == id).one_or_none()
            body = request.get_json()
            if not body:
                response = {"Message": "No input data provided"}
                return response, 400

            if 'age' in body:
                age = body["age"]
                now = datetime.now()
                created_at = f'{now.year - age}-{now.month}-{now.day} {now.hour}:{now.minute}:{now.second}'
                body.update({"created_at": created_at})
                del body['age']

            if palm:
                try:
                    data = palm_schema.load(body, partial=('location', 'max_banana_in_bundle',))
                except ValidationError as e:
                    return e.messages, 422
            else:
                response = {"Message": f"Not found palm with id: {id}"}
                return response, 404

            Palm.query.filter(Palm.id == id).update(body)
            db.session.commit()
            return palm_schema.dump(palm), 200

        elif request.method == 'DELETE':
            palm = Palm.query.filter(Palm.id == id).one_or_none()
            if palm:
                db.session.delete(palm)
                db.session.commit()
                response = {"Message": "Successfully deleted palm"}
                return response, 204
            else:
                response = {
                    "Message": f"Not found palm with id: {id}"
                }
                return response, 404

    @app.route("/palm", methods=["GET", "POST"])
    def handle_palm():
        if request.method == 'GET':
            palms = Palm.query.all()
            response = jsonify(palms_schema.dump(palms))
            return response

        if request.method == "POST":
            body = request.get_json()
            if not body:
                response = {"Message": "No input data provided"}
                return response, 400

            try:
                location = body["location"]
            except Exception as e:
                response = {'location': ['Missing data for required field.']}
                return response, 422

            try:
                max_banana_in_bundle = body["max_banana_in_bundle"]
            except Exception as e:
                response = {'max_banana_in_bundle': ['Missing data for required field.']}
                return response, 422

            palm = {
                "location": location,
                "max_banana_in_bundle": max_banana_in_bundle
            }

            if 'age' in body:
                age = body["age"]
                now = datetime.now()
                created_at = f'{now.year - age}-{now.month}-{now.day} {now.hour}:{now.minute}:{now.second}'
                palm.update({"created_at": created_at})

            palm = Palm(**palm)
            db.session.add(palm)
            db.session.commit()
            response = palm_schema.dump(Palm.query.get(palm.id))
            return response, 201
    return app
