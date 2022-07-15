from flask_marshmallow import Marshmallow

from application.models import Banana

ma = Marshmallow()


class BananaSchema(ma.Schema):
    class Meta:
        fields = ('id', 'color', 'origins')


banana_schema = BananaSchema()
bananas_schema = BananaSchema(many=True)
