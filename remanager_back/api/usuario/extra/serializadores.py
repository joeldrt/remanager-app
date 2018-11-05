from flask_restplus import fields
from remanager_back.api.restplus import api


fotos_extra = api.model('FotosExtra', {
    'picturesUrls': fields.List(fields.String, description='urls de las fotos del usuario')
})

profile_picture = api.model('ProfilePicture', {
    'profilePictureUrl': fields.String(description='foto de perfil actual del usuario')
})

usuario_extra = api.model('UsuarioExtra', {
    'id': fields.String(readOnly=True, description='Identificador unico de los datos extras del usuario'),
    'fechaAlta': fields.DateTime,
    'login': fields.String(required=True, description='Sobrenombre del usuario'),
    'profilePictureUrl': fields.String(description='Url de la foto de perfil'),
    'picturesUrls': fields.List(fields.String)
})
