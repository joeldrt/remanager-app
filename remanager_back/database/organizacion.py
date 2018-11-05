import mongoengine
from datetime import datetime

import remanager_back.database.mongo_digiall_utils as mongo_utils


class Organizacion(mongoengine.Document):
    fechaCreacion = mongoengine.DateTimeField(default=datetime.now)

    correoCreador = mongoengine.StringField()
    descripcion = mongoengine.StringField()
    nombre = mongoengine.StringField()

    def to_dict(self):
        return mongo_utils.mongo_to_dict_1(self)

    meta = {
        'db_alias': 'core',
        'collection': 'organizacion'
    }
