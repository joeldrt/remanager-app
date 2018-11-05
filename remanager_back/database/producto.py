import mongoengine
from datetime import datetime

import remanager_back.database.mongo_digiall_utils as mongo_utils


class ValorCampo(mongoengine.EmbeddedDocument):
    fechaCreacion = mongoengine.DateTimeField(default=datetime.now)

    nombre = mongoengine.StringField()
    valor = mongoengine.StringField()
    icono = mongoengine.StringField()
    tipoCampo = mongoengine.StringField()


class Producto(mongoengine.Document):
    fechaCreacion = mongoengine.DateTimeField(default=datetime.now)

    proyectoId = mongoengine.StringField()
    organizacionId = mongoengine.StringField()

    nombre = mongoengine.StringField()
    descripcion = mongoengine.StringField()
    estatus = mongoengine.StringField()
    correoCreador = mongoengine.StringField()
    idSeccion = mongoengine.StringField()
    precio = mongoengine.FloatField()
    tipoDeProducto = mongoengine.StringField()
    valoresCampos = mongoengine.ListField(mongoengine.EmbeddedDocumentField(ValorCampo))
    fotos = mongoengine.ListField(mongoengine.StringField())
    archivos = mongoengine.ListField(mongoengine.StringField())

    def to_dict(self):
        return mongo_utils.mongo_to_dict_1(self)

    meta = {
        'db_alias': 'core',
        'collection': 'producto'
    }
