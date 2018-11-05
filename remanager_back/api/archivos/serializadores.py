from flask_restplus import fields
from remanager_back.api.restplus import api


archivo = api.model('Archivo', {
    'value': fields.String(required=True, description='Datos del archivo en base 64'),
    'filename': fields.String(required=True, description='Nombre del archivo con extensión')
})


envio_archivos = api.model('EnvioArchivos', {
    'folder': fields.String(required=True, description='Folder del archivo a guardar'),
    'files': fields.List(fields.Nested(archivo), required=True, description='Archivos en base 64 a guardar')
})