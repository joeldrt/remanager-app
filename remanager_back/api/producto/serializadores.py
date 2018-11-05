from flask_restplus import fields
from remanager_back.api.restplus import api


valor_campo = api.model('ValorCampo', {
    'fechaCreacion': fields.DateTime,
    'nombre': fields.String(required=True, description='Nombre del campo'),
    'valor': fields.String(required=True, description='Valor del campo en string'),
    'icono': fields.String(description='Icono que representa al campo'),
    'tipoCampo': fields.String(description='Tipo de dato del valor')
})

producto = api.model('Producto', {
    'id': fields.String(readOnly=True, description='Id del producto'),
    'fechaCreacion': fields.DateTime,
    'proyectoId': fields.String(required=True, description='Id del proyecto al que pertenece el producto'),
    'organizacionId': fields.String(required=True, description='Id de la organización a la que pertenece el producto'),
    'nombre': fields.String(required=True, description='Nombre del producto'),
    'descripcion': fields.String(description='Descripción del proucto'),
    'estatus': fields.String(description='Estatus del producto "DISPONIBLE", "BLOQUEADO", "APARTADO", "VENDIDO"'),
    'correoCreador': fields.String(required=True, description='Correo del usuario que creó este producto'),
    'idSeccion': fields.String(description='ID del polígono del svg del padre que hace referencia a éste producto'),
    'precio': fields.Float(description='Precio del producto'),
    'tipoDeProducto': fields.String(description='Tipo de producto'),
    'valoresCampos': fields.List(fields.Nested(valor_campo)),
    'fotos': fields.List(fields.String, description='lista urls de fotos asociadas a ese producto'),
    'archivos': fields.List(fields.String, description='lista de urls de archivos asociados a ese producto')
})
