from flask_restplus import fields
from remanager_back.api.restplus import api


class NullableString(fields.String):
    __schema_type__ =['string', 'null']
    __schema_example__ = 'nullable string'


proyecto = api.model('Proyecto', {
    'id': fields.String(readOnly=True, description='Id del proyecto'),
    'fechaCreacion': fields.DateTime,
    'nombre': fields.String(required=True, description='Nombre del proyecto'),
    'descripcion': fields.String(description='Descripcion del proyecto'),
    'correoCreador': fields.String(description='Correo del usuario que ha creado el proyecto'),
    'idSeccion': NullableString(description='Id de la sección del SVG del padre que lo identifica'),
    'svgId': NullableString(description='Id del SVG de éste proyecto'),
    'organizacionId': fields.String(description='Id de la organización dueña de este proyecto'),
    'padreId': fields.String(description='Id del proyecto padre')
})
