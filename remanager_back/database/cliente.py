import mongoengine
from datetime import datetime

import remanager_back.database.mongo_digiall_utils as mongo_utils


class Cliente(mongoengine.Document):
    fechaAlta = mongoengine.DateTimeField(default=datetime.now)
    organizacionId = mongoengine.StringField(required=True)
    correoVendedor = mongoengine.StringField(required=True)
    email = mongoengine.StringField(required=True)
    nombre = mongoengine.StringField(required=True)
    apellidos = mongoengine.StringField()
    direccion = mongoengine.StringField()
    fechaNacimiento = mongoengine.DateTimeField()
    telefono = mongoengine.StringField(required=True)

    def to_dict(self):
        return mongo_utils.mongo_to_dict_1(self)

    @mongoengine.queryset_manager
    def objects(cls, queryset):
        return queryset.order_by('nombre')

    meta = {
        'db_alias': 'core',
        'collection': 'cliente'
    }
