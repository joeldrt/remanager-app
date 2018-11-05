from flask_restplus import fields
from remanager_back.api.restplus import api

from remanager_back.api.contrato.serializadores import resumen_contrato


cliente = api.model('Cliente', {
    'id': fields.String(readOnly=True, description='Id del cliente'),
    'fechaAlta': fields.DateTime,
    'organizacionId': fields.String(required=True, description='Id de la organizacion a la que pertenece el cliente'),
    'correoVendedor': fields.String(required=True, description='Correo del vendedor a quien se le asocia el cliente'),
    'email': fields.String(required=True, description='Email del cliente'),
    'nombre': fields.String(required=True, description='Nombre del cliente'),
    'apellidos': fields.String(description='Apellidos del cliente'),
    'direccion': fields.String(description='Dirección del cliente'),
    'fechaNacimiento': fields.String(description='Fecha de nacimiento del cliente'),
    'telefono': fields.String(required=True, description='Teléfono del cliente')
})

resumen_cliente_contratos = api.model('ResumenClienteContrato', {
    'cliente': fields.Nested(cliente),
    'resumen_contratos': fields.List(fields.Nested(resumen_contrato), description='lista de contratos del cliente')
})
