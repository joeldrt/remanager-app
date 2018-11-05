import logging
from datetime import datetime

from flask import request
from flask_restplus import Resource, abort, reqparse
from flask_jwt_extended import (jwt_required, get_jwt_identity)
from remanager_back.api.contrato.servicios import crear_contrato, obtener_contratos,\
    obtener_contratos_por_correo_vendedor, obtener_contrato_por_contrato_id,\
    obtener_contrato_por_contrato_id_y_correo_vendedor, borrar_contrato, desactivar_contrato, agregar_pago_real
from remanager_back.api.cliente.servicios import obtener_cliente_por_id, obtener_cliente_por_id_correo_vendedor
from remanager_back.api.producto.servicios import obtener_producto_por_id
from remanager_back.api.contrato.serializadores import contrato, pago_programado, pago_real
from remanager_back.api.restplus import api

from remanager_back.data_auth.models import UserModel

from remanager_back.settings import AUTHORITY_ADMIN, AUTHORITY_ROOT

log = logging.getLogger(__name__)

ns = api.namespace('contratos', description='Servicios para manejar los contratos')


@ns.route('/')
class Contrato(Resource):

    @api.marshal_with(contrato)
    @api.expect(contrato)
    @jwt_required
    def post(self):
        login = get_jwt_identity()
        current_user = UserModel.find_by_login(login)

        data = request.json

        if current_user.has_authority(AUTHORITY_ADMIN) or current_user.has_authority(AUTHORITY_ROOT):
            client = obtener_cliente_por_id(data.get('clienteId'))
        else:
            client = obtener_cliente_por_id_correo_vendedor(correo_vendedor=current_user.email,
                                                            cliente_id=data.get('clienteId'))

        if not client:
            abort(404, 'No existe el cliente con ese Id')

        product = obtener_producto_por_id(data.get('productoId'))

        if not product:
            abort(404, 'No existe un producto con ese Id')

        try:
            contract = crear_contrato(tipo=data.get('tipo'),
                                      cliente_id=data.get('clienteId'),
                                      producto_id=data.get('productoId'),
                                      correo_vendedor=current_user.email,
                                      dias_validez=data.get('diasValidez'),
                                      pagos_programados=data.get('pagosProgramados'))
            return contract.to_dict()
        except Exception as exception:
            abort(500, 'Error del servidor al crear el contrato')

    @api.marshal_list_with(contrato)
    @jwt_required
    def get(self):
        login = get_jwt_identity()
        current_user = UserModel.find_by_login(login)

        try:
            if current_user.has_authority(AUTHORITY_ADMIN) or current_user.has_authority(AUTHORITY_ROOT):
                contratos_objs = obtener_contratos()
            else:
                contratos_objs = obtener_contratos_por_correo_vendedor(correo_vendedor=current_user.email)

            contratos = [
                contrato.to_dict() for contrato in contratos_objs
            ]
            return contratos
        except Exception as exception:
            abort(500, 'Error del servidor al recuperar los clientes')


desactivar_parser = reqparse.RequestParser()
desactivar_parser.add_argument('desactivar', type=bool, location='args')


@ns.route('/<string:contrato_id>')
class ContratoActions(Resource):

    @api.marshal_with(contrato)
    @jwt_required
    def get(self, contrato_id):
        login = get_jwt_identity()
        current_user = UserModel.find_by_login(login)

        try:
            if current_user.has_authority(AUTHORITY_ADMIN) or current_user.has_authority(AUTHORITY_ROOT):
                contract = obtener_contrato_por_contrato_id(contrato_id)
            else:
                contract = obtener_contrato_por_contrato_id_y_correo_vendedor(correo_vendedor=current_user.email,
                                                                              contrato_id=contrato_id)
            if not contract:
                abort(404, 'No se encontró el contrato con ese Id')

            return contract.to_dict()
        except Exception as exception:
            abort(500, 'Error del servidor al recuperar el contrato')

    @api.marshal_with(contrato)
    @api.expect(desactivar_parser)
    @jwt_required
    def put(self, contrato_id):
        login = get_jwt_identity()
        current_user = UserModel.find_by_login(login)

        argumentos = desactivar_parser.parse_args()

        if argumentos['desactivar']:
            try:
                if current_user.has_authority(AUTHORITY_ADMIN) or current_user.has_authority(AUTHORITY_ROOT):
                    contract = obtener_contrato_por_contrato_id(contrato_id)
                else:
                    contract = obtener_contrato_por_contrato_id_y_correo_vendedor(correo_vendedor=current_user.email,
                                                                                  contrato_id=contrato_id)
                if not contract:
                    abort(404, 'No se encontró el contrato con ese Id')

                contract = desactivar_contrato(contrato_id)

                return contract.to_dict
            except Exception as exception:
                abort(500, 'Error del servidor al desactivar el contrato')
        else:
            abort(501, 'el método no está implementado')

    @jwt_required
    def delete(self, contrato_id):
        login = get_jwt_identity()
        current_user = UserModel.find_by_login(login)

        if not current_user.has_authority(AUTHORITY_ADMIN) and not current_user.has_authority(AUTHORITY_ROOT):
            abort(403, 'No cuenta con los permisos necesarios para realizar esta acción')

        try:
            borrar_contrato(contrato_id)
            return {'message': 'Contrato borrado exitosamente'}
        except Exception as exception:
            abort(500, 'Error del servidor al borrar el contrato')


@ns.route('/<string:contrato_id>/pagosprogramados')
class PagoProgramado(Resource):

    @api.marshal_list_with(pago_programado)
    @jwt_required
    def get(self, contrato_id):
        login = get_jwt_identity()
        current_user = UserModel.find_by_login(login)

        try:
            if current_user.has_authority(AUTHORITY_ADMIN) or current_user.has_authority(AUTHORITY_ROOT):
                contract = obtener_contrato_por_contrato_id(contrato_id)
            else:
                contract = obtener_contrato_por_contrato_id_y_correo_vendedor(correo_vendedor=current_user.email,
                                                                              contrato_id=contrato_id)
            if not contract:
                abort(404, 'No se encontró el contrato con ese Id')

            pagos_programados_objs = contract.pagosProgramados

            pagos_programados = [
                pago_programado.to_dict() for pago_programado in pagos_programados_objs
            ]

            return pagos_programados

        except Exception as exception:
            abort(500, 'Error del servidor al recuperar los pagos programados para ese contrato')


@ns.route('/<string:contrato_id>/pagosreales')
class PagoReal(Resource):

    @api.marshal_with(pago_real)
    @api.expect(pago_real)
    @jwt_required
    def post(self, contrato_id):
        login = get_jwt_identity()
        current_user = UserModel.find_by_login(login)

        try:
            if current_user.has_authority(AUTHORITY_ADMIN) or current_user.has_authority(AUTHORITY_ROOT):
                contract = obtener_contrato_por_contrato_id(contrato_id)
            else:
                contract = obtener_contrato_por_contrato_id_y_correo_vendedor(correo_vendedor=current_user.email,
                                                                              contrato_id=contrato_id)
            if not contract:
                abort(404, 'No se encontró el contrato con ese Id')

            data = request.json

            pay = agregar_pago_real(contrato_id=contrato_id, data=data)

            return pay.to_dict()
        except Exception as exception:
            abort(500, 'Error del servidor al generar el pago real para ese contrato')
