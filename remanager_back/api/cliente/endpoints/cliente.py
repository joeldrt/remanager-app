import logging
from datetime import datetime

from flask import request
from flask_restplus import Resource, abort
from flask_jwt_extended import (jwt_required, get_jwt_identity)
from remanager_back.api.cliente.servicios import crear_cliente, obtener_cliente_por_id,\
    obtener_cliente_por_id_correo_vendedor, editar_cliente, borrar_cliente_por_id,\
    obtener_todos_los_clientes_por_organizacion_id, obtener_clientes_por_correo_vendedor
from remanager_back.api.contrato.servicios import obtener_contratos_por_cliente_id,\
    obtener_resumen_contratos_por_cliente
from remanager_back.api.cliente.serializadores import cliente, resumen_cliente_contratos
from remanager_back.api.restplus import api

from remanager_back.data_auth.models import UserModel

from remanager_back.settings import AUTHORITY_ADMIN, AUTHORITY_ROOT

log = logging.getLogger(__name__)

ns = api.namespace('clientes', description='Servicios para manejar los cliente')


@ns.route('/')
class Clientes(Resource):

    @api.marshal_with(cliente)
    @api.expect(cliente)
    @jwt_required
    def post(self):
        login = get_jwt_identity()
        current_user = UserModel.find_by_login(login)

        data = request.json

        try:
            cliente = crear_cliente(organizacion_id=current_user.organizationId,
                                    correo_vendedor=current_user.email,
                                    email=data.get('email'),
                                    nombre=data.get('nombre'),
                                    apellidos=data.get('apellidos'),
                                    direccion=data.get('direccion'),
                                    fecha_nacimiento=datetime.strptime(
                                        data.get('fechaNacimiento'), '%Y-%m-%dT%H:%M:%S') if data.get('fechaNacimiento') else None,
                                    telefono=data.get('telefono'))
        except Exception as exception:
            abort(500, 'Error del servidor al persistir el cliente')

        return cliente.to_dict()

    @api.marshal_list_with(cliente)
    @jwt_required
    def get(self):
        login = get_jwt_identity()
        current_user = UserModel.find_by_login(login)

        if current_user.has_authority(AUTHORITY_ADMIN):
            clientes_obj = obtener_todos_los_clientes_por_organizacion_id(organizacion_id=current_user.organizationId)
        else:
            clientes_obj = obtener_clientes_por_correo_vendedor(correo_vendedor=current_user.email)

        clientes = [
            cliente.to_dict() for cliente in clientes_obj
        ]

        return clientes


@ns.route('/<string:cliente_id>')
class ClientesPorId(Resource):

    @api.marshal_with(cliente)
    @jwt_required
    def get(self, cliente_id):
        login = get_jwt_identity()
        current_user = UserModel.find_by_login(login)

        if current_user.has_authority(AUTHORITY_ADMIN) or current_user.has_authority(AUTHORITY_ROOT):
            cliente = obtener_cliente_por_id(cliente_id=cliente_id)
        else:
            cliente = obtener_cliente_por_id_correo_vendedor(correo_vendedor=current_user.email, cliente_id=cliente_id)

        if not cliente:
            abort(404, 'No existe ningún cliente con ese Id')

        return cliente.to_dict()

    @api.marshal_with(cliente)
    @api.expect(cliente)
    @jwt_required
    def put(self, cliente_id):
        login = get_jwt_identity()
        current_user = UserModel.find_by_login(login)

        if current_user.has_authority(AUTHORITY_ADMIN) or current_user.has_authority(AUTHORITY_ROOT):
            cliente = obtener_cliente_por_id(cliente_id=cliente_id)
        else:
            cliente = obtener_cliente_por_id_correo_vendedor(correo_vendedor=current_user.email, cliente_id=cliente_id)

        if not cliente:
            abort(404, 'No existe ningún cliente con ese Id')

        data = request.json

        if data.get('fechaNacimiento') and data.get('fechaNacimiento') != "":
            try:
                fecha_nacimiento = datetime.strptime(data.get('fechaNacimiento'), '%Y-%m-%dT%H:%M:%S.%fZ')
                if fecha_nacimiento < datetime.strptime('1900-01-01', '%Y-%m-%d'):
                    fecha_nacimiento = None
            except Exception as exception:
                fecha_nacimiento = None
        else:
            fecha_nacimiento = None

        try:
            client = editar_cliente(cliente_id=cliente_id,
                                    email=data.get('email'),
                                    nombre=data.get('nombre'),
                                    apellidos=data.get('apellidos'),
                                    fecha_nacimiento=fecha_nacimiento,
                                    direccion=data.get('direccion'),
                                    telefono=data.get('telefono'))
            return client.to_dict()
        except Exception as exception:
            abort(500, 'Error del servidor al editar el cliente')

    @jwt_required
    def delete(self, cliente_id):
        login = get_jwt_identity()
        current_user = UserModel.find_by_login(login)

        if current_user.has_authority(AUTHORITY_ADMIN) or current_user.has_authority(AUTHORITY_ROOT):
            cliente = obtener_cliente_por_id(cliente_id=cliente_id)
        else:
            cliente = obtener_cliente_por_id_correo_vendedor(correo_vendedor=current_user.email, cliente_id=cliente_id)

        if not cliente:
            abort(404, 'No existe ningún cliente con ese Id')

        try:
            borrar_cliente_por_id(cliente_id=cliente_id)
        except Exception as exception:
            abort(500, 'Error del servidor al borrar el cliente')

        return {'message': 'Cliente borrado exitosamente'}


@ns.route('/<string:cliente_id>/contratos')
class ClientesPorId(Resource):

    @jwt_required
    def get(self, cliente_id):
        login = get_jwt_identity()
        current_user = UserModel.find_by_login(login)

        if current_user.has_authority(AUTHORITY_ADMIN) or current_user.has_authority(AUTHORITY_ROOT):
            client = obtener_cliente_por_id(cliente_id)
        else:
            client = obtener_cliente_por_id_correo_vendedor(correo_vendedor=current_user.email,
                                                            cliente_id=cliente_id)

        if not client:
            abort(404, 'No existe el cliente con ese Id')

        try:
            contratos_objs = obtener_contratos_por_cliente_id(cliente_id=cliente_id)
            contratos = [
                contrato.to_dict() for contrato in contratos_objs
            ]
            return contratos
        except Exception as exception:
            abort(500, 'Error del servidor al obtener los contratos del cliente')


@ns.route('/<string:cliente_id>/resumencontratos')
class ClienteResumenContratos(Resource):

    @api.marshal_with(resumen_cliente_contratos)
    @jwt_required
    def get(self, cliente_id):
        login = get_jwt_identity()
        current_user = UserModel.find_by_login(login)

        if current_user.has_authority(AUTHORITY_ADMIN) or current_user.has_authority(AUTHORITY_ROOT):
            client = obtener_cliente_por_id(cliente_id)
        else:
            client = obtener_cliente_por_id_correo_vendedor(correo_vendedor=current_user.email,
                                                            cliente_id=cliente_id)

        if not client:
            abort(404, 'No existe el cliente con ese Id')

        try:
            resumen_cliente_contratos_obj = obtener_resumen_contratos_por_cliente(cliente_id=cliente_id)
            return resumen_cliente_contratos_obj
        except Exception as exception:
            abort(500, 'Error del servidor al recuperar el resumen de los contratos por cliente')
