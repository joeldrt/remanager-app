import mongoengine
from datetime import datetime

import remanager_back.database.mongo_digiall_utils as mongo_utils


class Punto(mongoengine.EmbeddedDocument):
    x = mongoengine.FloatField()
    y = mongoengine.FloatField()


class Poligono(mongoengine.EmbeddedDocument):
    puntos = mongoengine.StringField()
    genUid = mongoengine.LongField()
    arregloPuntos = mongoengine.ListField(mongoengine.EmbeddedDocumentField(Punto))


class Svg(mongoengine.Document):
    fechaAlta = mongoengine.DateTimeField(default=datetime.now)

    nombre = mongoengine.StringField(required=True)
    imagenContentType = mongoengine.StringField()
    imagen = mongoengine.StringField()
    width = mongoengine.FloatField()
    height = mongoengine.FloatField()
    codigoContentType = mongoengine.StringField()
    codigo = mongoengine.StringField()
    proyectoId = mongoengine.StringField()
    poligonos = mongoengine.ListField(mongoengine.EmbeddedDocumentField(Poligono))

    def to_dict(self):
        return mongo_utils.mongo_to_dict_1(self)

    meta = {
        'db_alias': 'core',
        'collection': 'svg'
    }
