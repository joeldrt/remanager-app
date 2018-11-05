from flask_restplus import fields
from remanager_back.api.restplus import api


proyecto = api.model('Proyecto', {
    'id': fields.String(readOnly=True, description='Id del proyecto'),
    'fechaCreacion': fields.DateTime,
    'nombre': fields.String(required=True, description='Nombre del proyecto'),
    'descripcion': fields.String(description='Descripcion del proyecto'),
    'correoCreador': fields.String(description='Correo del usuario que ha creado el proyecto'),
    'idSeccion': fields.String(description='Id de la sección del SVG del padre que lo identifica'),
    'svgId': fields.String(description='Id del SVG de éste proyecto'),
    'organizacionId': fields.String(description='Id de la organización dueña de este proyecto'),
    'padreId': fields.String(description='Id del proyecto padre')
})