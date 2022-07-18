from flask_marshmallow import Marshmallow

from application.models import Banana

ma = Marshmallow()


class BananaSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Banana
        load_instance = True


banana_schema = BananaSchema()
bananas_schema = BananaSchema(many=True)
