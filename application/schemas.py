from flask_marshmallow import Marshmallow

from application.models import Banana, Palm

ma = Marshmallow()


class BananaSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Banana
        load_instance = True


class PalmSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Palm
        load_instance = True


banana_schema = BananaSchema()
bananas_schema = BananaSchema(many=True)

palm_schema = PalmSchema()
palms_schema = PalmSchema(many=True)
