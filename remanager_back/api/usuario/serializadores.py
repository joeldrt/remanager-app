from flask_restplus import fields
from remanager_back.api.restplus import api


autorizaciones = api.model('Autorizaciones', {
    'id': fields.Integer(readOnly=True, description='Id del permiso'),
    'authority_name': fields.String(description='Nombre del permiso asociado')
})

usuario = api.model('Usuario', {
    'id': fields.Integer(readOnly=True, description='Identificador unico del usuario'),
    'login': fields.String(required=True, description='Sobrenombre del usuario'),
    'email': fields.String(required=True, description='Coreo electrónico del usuario'),
    'password': fields.String(required=True, description='Password del usuario'),
    'firstName': fields.String(required=True, description='Nombre del usuario'),
    'lastName': fields.String(description='Apellidos del usuario'),
    'activated': fields.Boolean(description='Status del usuario en cuanto activación'),
    'organizationId': fields.String(description='Id de la Organización a la que pertenece el usuario'),
    'authorities': fields.List(fields.String)
})
