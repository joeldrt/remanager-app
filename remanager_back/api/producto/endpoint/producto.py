import logging
from datetime import datetime

from flask import request
from flask_restplus import Resource, reqparse, abort
from flask_jwt_extended import (jwt_required, get_jwt_identity)
from remanager_back.api.producto.servicios import crear_producto, obtener_productos,\
    obtener_productos_por_organizacion_id, obtener_producto_por_id, obtener_producto_por_id_y_organizacion_id,\
    editar_producto, borrar_producto_por_id, obtener_productos_por_proyecto_id,\
    obtener_productos_por_organizacion_id_y_proyecto_id
from remanager_back.api.contrato.servicios import obtener_contratos_por_producto_id,\
    obtener_contratos_por_producto_id_y_correo_vendedor
from remanager_back.api.producto.serializadores import producto
from remanager_back.api.contrato.serializadores import contrato
from remanager_back.api.restplus import api

from remanager_back.data_auth.models import UserModel

from remanager_back.settings import AUTHORITY_ADMIN, AUTHORITY_ROOT

log = logging.getLogger(__name__)

ns = api.namespace('productos', description='Servicios para manejar los productos')


buscar_productos_parser = reqparse.RequestParser()
buscar_productos_parser.add_argument('proyectoId', type=str, location='args')

@ns.route('/')
class Productos(Resource):

    @api.marshal_with(producto)
    @api.expect(producto)
    @jwt_required
    def post(self):
        login = get_jwt_identity()
        current_user = UserModel.find_by_login(login)

        if not current_user.has_authority(AUTHORITY_ADMIN) and not current_user.has_authority(AUTHORITY_ROOT):
            abort(401, 'No se cuentan con los permisos necesarios para crear un producto')

        data = request.json

        try:
            product = crear_producto(organizacion_id=current_user.organizationId,
                                     proyecto_id=data.get('proyectoId'),
                                     correo_creador=current_user.email,
                                     id_seccion=data.get('idSeccion'),
                                     nombre=data.get('nombre'),
                                     descripcion=data.get('descripcion'),
                                     precio=data.get('precio'),
                                     tipo_de_producto=data.get('tipoDeProducto'),
                                     estatus=data.get('estatus'),
                                     valores_campos=data.get('valoresCampos'),
                                     fotos=data.get('fotos'),
                                     archivos=data.get('archivos'))
            return product.to_dict()
        except Exception as exception:
            abort(500, 'Error del servidor al guardar el producto')

    @api.marshal_list_with(producto)
    @api.expect(buscar_productos_parser)
    @jwt_required
    def get(self):
        login = get_jwt_identity()
        current_user = UserModel.find_by_login(login)

        data = buscar_productos_parser.parse_args()

        try:
            if not data['proyectoId']:
                if current_user.has_authority(AUTHORITY_ADMIN) or current_user.has_authority(AUTHORITY_ROOT):
                    productos_obj = obtener_productos()
                else:
                    productos_obj = obtener_productos_por_organizacion_id(organizacion_id=current_user.organizationId)
            else:
                if current_user.has_authority(AUTHORITY_ADMIN) or current_user.has_authority(AUTHORITY_ROOT):
                    productos_obj = obtener_productos_por_proyecto_id(data['proyectoId'])
                else:
                    productos_obj = obtener_productos_por_organizacion_id_y_proyecto_id(
                        organizacion_id=current_user.organizationId,
                        proyecto_id=data['proyectoId'])
            productos = [
                producto.to_dict() for producto in productos_obj
            ]

            return productos
        except Exception as exception:
            abort(500, 'Error del servidor al recuperar los productos')


@ns.route('/<string:producto_id>')
class ProductosActions(Resource):

    @api.marshal_with(producto)
    @jwt_required
    def get(self, producto_id):
        login = get_jwt_identity()
        current_user = UserModel.find_by_login(login)

        if current_user.has_authority(AUTHORITY_ADMIN) or current_user.has_authority(AUTHORITY_ROOT):
            product = obtener_producto_por_id(producto_id=producto_id)
        else:
            product = obtener_producto_por_id_y_organizacion_id(producto_id=producto_id,
                                                                organizacion_id=current_user.organizationId)
        if not product:
            abort(404, 'No se encontró un producto con ese Id')

        return product.to_dict()

    @api.marshal_with(producto)
    @api.expect(producto)
    @jwt_required
    def put(self, producto_id):
        login = get_jwt_identity()
        current_user = UserModel.find_by_login(login)

        if not current_user.has_authority(AUTHORITY_ADMIN) and not current_user.has_authority(AUTHORITY_ROOT):
            abort(401, 'No se cuentan con los permisos necesarios para crear un producto')

        data = request.json

        try:
            product = editar_producto(producto_id=producto_id,
                                      organizacion_id=current_user.organizationId if current_user.organizationId else data.get('organizacion_id'),
                                      proyecto_id=data.get('proyectoId'),
                                      correo_creador=current_user.email,
                                      id_seccion=data.get('idSeccion'),
                                      nombre=data.get('nombre'),
                                      descripcion=data.get('descripcion'),
                                      precio=data.get('precio'),
                                      tipo_de_producto=data.get('tipoDeProducto'),
                                      estatus=data.get('estatus'),
                                      valores_campos=data.get('valoresCampos'),
                                      fotos=data.get('fotos'),
                                      archivos=data.get('archivos'))
            return product.to_dict()
        except Exception as exception:
            abort(500, 'Error del servidor al editar el producto')

    @jwt_required
    def delete(self, producto_id):
        login = get_jwt_identity()
        current_user = UserModel.find_by_login(login)

        if not current_user.has_authority(AUTHORITY_ADMIN) and not current_user.has_authority(AUTHORITY_ROOT):
            abort(401, 'No se cuentan con los permisos necesarios para borrar el producto')

        try:
            borrar_producto_por_id(producto_id)
        except Exception as exception:
            abort(500, 'Error del servidor al borrar el producto')

        return {'message': 'Producto borrado exitosamente'}


@ns.route('/<string:producto_id>/contratos')
class ProductoContratos(Resource):

    @api.marshal_list_with(contrato)
    @jwt_required
    def get(self, producto_id):
        login = get_jwt_identity()
        current_user = UserModel.find_by_login(login)

        try:
            if current_user.has_authority(AUTHORITY_ADMIN) or current_user.has_authority(AUTHORITY_ROOT):
                contracts = obtener_contratos_por_producto_id(producto_id=producto_id)
            else:
                contracts = obtener_contratos_por_producto_id_y_correo_vendedor(producto_id=producto_id,
                                                                                correo_vendedor=current_user.email)

            contratos = [
                contrato.to_dict() for contrato in contracts
            ]

            return contratos
        except Exception as exception:
            abort(500, 'Error del servidor al recuperar los contratos relacionados con el producto')
