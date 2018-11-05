import logging

from flask import request
from flask_restplus import Resource, reqparse, abort
from flask_jwt_extended import (jwt_required, get_jwt_identity)
from remanager_back.api.proyecto.servicios import obtener_proyecto_por_id, obtener_proyectos_por_organizacion, \
    obtener_proyectos_root_por_organizacion, obtener_proyectos_por_padreId
from remanager_back.api.producto.servicios import obtener_productos_por_proyecto_id
from remanager_back.api.proyecto.serializadores import proyecto
from remanager_back.api.producto.serializadores import producto
from remanager_back.api.restplus import api

from remanager_back.database.proyecto import Proyecto
from remanager_back.data_auth.models import UserModel

log = logging.getLogger(__name__)

ns = api.namespace('proyectos', description='Servicios para manejar los proyectos')


parser = reqparse.RequestParser()
parser.add_argument('proyecto_raiz', type=bool, location='args')
parser.add_argument('padre_id', type=str, location='args')

@ns.route('/')
class AddProyecto(Resource):

    @api.marshal_with(proyecto)
    @api.expect(proyecto)
    @jwt_required
    def post(self):
        login = get_jwt_identity()
        current_user = UserModel.find_by_login(login)

        data = request.json

        proyecto_obj = Proyecto()
        proyecto_obj.nombre = data.get('nombre')
        proyecto_obj.descripcion = data.get('descripcion')
        proyecto_obj.correoCreador = current_user.email
        proyecto_obj.idSeccion = data.get('idSeccion')
        proyecto_obj.svgId = data.get('svgId')
        proyecto_obj.organizacionId = current_user.organizationId
        proyecto_obj.padreId = data.get('padreId')

        try:
            proyecto_obj.save()
        except Exception as exception:
            abort(500, 'Error del servidor al tratar de persistir el proyecto')

        return proyecto_obj.to_dict()

    @api.marshal_list_with(proyecto)
    @api.expect(parser)
    @jwt_required
    def get(self):
        login = get_jwt_identity()
        current_user = UserModel.find_by_login(login)

        data = parser.parse_args()

        if data['proyecto_raiz']:
            proyectos_obj = obtener_proyectos_root_por_organizacion(organizacion_id=current_user.organizationId)
        else:
            if data['padre_id'] is None:
                proyectos_obj = obtener_proyectos_por_organizacion(organizacion_id=current_user.organizationId)
            else:
                proyectos_obj = obtener_proyectos_por_padreId(organizacion_id=current_user.organizationId,
                                                              padre_id=data['padre_id'])

        proyectos = [
            proyecto.to_dict() for proyecto in proyectos_obj
        ]
        return proyectos



@ns.route('/<string:proyecto_id>')
class AccionesProyectoRegistrado(Resource):

    @jwt_required
    def delete(self, proyecto_id):
        login = get_jwt_identity()
        current_user = UserModel.find_by_login(login)

        proyecto = obtener_proyecto_por_id(organizacion_id=current_user.organizationId, proyecto_id=proyecto_id)

        if proyecto is None:
            abort(404, 'No existe un proyecto  con ese Id para la organización del usuario')

        try:
            proyecto.delete()
        except Exception as exception:
            abort(500, 'Error del servidor al tratar de borrar el proyecto con el Id: {}'.format(proyecto_id))
        return {'message': 'Proyecto with id: {} successfully deleted'.format(proyecto_id)}, 200

    @api.marshal_with(proyecto)
    @api.expect(proyecto)
    @jwt_required
    def put(self, proyecto_id):
        login = get_jwt_identity()
        current_user = UserModel.find_by_login(login)

        proyecto_obj = obtener_proyecto_por_id(organizacion_id=current_user.organizationId, proyecto_id=proyecto_id)

        if proyecto is None:
            return {'message': 'Proyecto {} doesnt exist'.format(proyecto_id)}, 401

        data = request.json

        proyecto_obj.nombre = data.get('nombre')
        proyecto_obj.descripcion = data.get('descripcion')
        proyecto_obj.correo_creador = data.get('correo_creador')
        proyecto_obj.id_seccion = data.get('id_seccion')
        proyecto_obj.svg_id = data.get('svg_id')
        proyecto_obj.organizacion_id = data.get('organizacion_id')
        proyecto_obj.padre_id = data.get('padre_id')

        try:
            edited_proyecto = proyecto_obj.save()
        except Exception as exception:
            abort(500, 'Error del servidor al tratar de borrar el proyecto con el Id: {}'.format(proyecto_id))
        return edited_proyecto.to_dict()

    @api.marshal_with(proyecto)
    @jwt_required
    def get(self, proyecto_id):
        login = get_jwt_identity()
        current_user = UserModel.find_by_login(login)
        proyecto_obj = obtener_proyecto_por_id(organizacion_id=current_user.organizationId, proyecto_id=proyecto_id)
        if proyecto_obj is None:
            abort(404, 'No existe un proyecto con ese Id para la organización del usuario')
        return proyecto_obj.to_dict()


@ns.route('/<string:proyecto_id>/productos')
class ProyectoProductos(Resource):

    @api.marshal_list_with(producto)
    @jwt_required
    def get(self, proyecto_id):
        login = get_jwt_identity()
        current_user = UserModel.find_by_login(login)

        try:
            productos_objs = obtener_productos_por_proyecto_id(proyecto_id=proyecto_id)
            productos = [
                producto.to_dict() for producto in productos_objs
            ]
            return productos
        except Exception as exception:
            abort(500, 'Error del servidor al recuperar los productos del proyecto')
