from flask_restplus import fields
from remanager_back.api.restplus import api

from remanager_back.api.producto.serializadores import producto


pago_real = api.model('PagoReal', {
    'uuid': fields.String(readOnly=True, description='uuid del pago real'),
    'fechaCreacion': fields.DateTime,
    'monto': fields.Float(required=True, description='Monto del pago real'),
    'archivos': fields.List(fields.String, description='Lista de archivos asociados al pago real'),
    'validado': fields.Boolean(description='Status del pago real, modificable por el responsable de finanzas o admin'),
    'correoQueValida': fields.String(description='Correo de quien valida el pago, debe ser de finanzas')
})

pago_programado = api.model('PagoProgramado', {
    'uuid': fields.String(readOnly=True, description='uuid del pago programado'),
    'fechaCompromisoPago': fields.DateTime(required=True, description='Fecha en la que el cliente se compromete a pagar'),
    'monto': fields.Float(required=True, description='Monto del pago programado')
})

contrato = api.model('Contrato', {
    'id': fields.String(readOnly=True, description='Id del contrato'),
    'fechaCreacion': fields.DateTime,
    'activo': fields.Boolean(description='Muestra si el contrato se encuentra activo o no se debe tomar en cuenta'),
    'tipo': fields.String(description='Tipo de contrato'),
    'clienteId': fields.String(required=True, description='Id del cliente asociado con este contrato'),
    'productoId': fields.String(required=True, description='Id del producto asociado con este contrato'),
    'correoVendedor': fields.String(description='Correo del vendedor que generó este contrato'),
    'diasValidez': fields.Integer(description='Dias de validez del contrato'),
    'observaciones': fields.String(description='Observaciones sobre el contacto'),
    'pagosProgramados': fields.List(fields.Nested(pago_programado)),
    'pagosReales': fields.List(fields.Nested(pago_real))
})

resumen_contrato = api.model('ResumenContrato', {
    'contrato': fields.Nested(contrato, description='Contrato del resumen'),
    'producto': fields.Nested(producto, description='Producto del resumen')
})


