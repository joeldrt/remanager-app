from flask_restplus import fields
from remanager_back.api.restplus import api


login = api.model('Login', {
    'login': fields.String(required=True, description='Sobrenombre del usuario'),
    'password': fields.String(required=True, description='Password del usuario')
})

access_token = api.model('Access Token', {
    'id_token': fields.String(required=True, description='Token del usuario autenticado')
})