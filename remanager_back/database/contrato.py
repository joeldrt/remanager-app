import mongoengine
from datetime import datetime
from passlib.hash import pbkdf2_sha256 as sha256

import remanager_back.database.mongo_digiall_utils as mongo_utils


class PagoReal(mongoengine.EmbeddedDocument):
    uuid = mongoengine.StringField(default=sha256.hash(str(datetime.now)))
    fechaCreacion = mongoengine.DateTimeField(default=datetime.now)
    monto = mongoengine.FloatField()
    archivos = mongoengine.ListField(mongoengine.StringField())
    validado = mongoengine.BooleanField(default=False)
    correoQueValida = mongoengine.StringField()

    def to_dict(self):
        return mongo_utils.mongo_to_dict_1(self)


class PagoProgramado(mongoengine.EmbeddedDocument):
    uuid = mongoengine.StringField(default=sha256.hash(str(datetime.now)))
    fechaCompromisoPago = mongoengine.DateTimeField()
    monto = mongoengine.FloatField()

    def to_dict(self):
        return mongo_utils.mongo_to_dict_1(self)


class Contrato(mongoengine.Document):
    fechaCreacion = mongoengine.DateTimeField(default=datetime.now)

    activo = mongoengine.BooleanField(default=True)

    tipo = mongoengine.StringField()

    clienteId = mongoengine.StringField()
    productoId = mongoengine.StringField()

    correoVendedor = mongoengine.StringField()
    diasValidez = mongoengine.IntField()

    observaciones = mongoengine.StringField()

    pagosProgramados = mongoengine.ListField(mongoengine.EmbeddedDocumentField(PagoProgramado))
    pagosReales = mongoengine.ListField(mongoengine.EmbeddedDocumentField(PagoReal))

    def to_dict(self):
        return mongo_utils.mongo_to_dict_1(self)

    @mongoengine.queryset_manager
    def objects(doc_cls, queryset):
        return queryset.order_by('-fechaCreacion')

    meta = {
        'db_alias': 'core',
        'collection': 'contrato'
    }
