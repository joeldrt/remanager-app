import logging

from flask import request
from flask_restplus import Resource, abort
from flask_jwt_extended import (jwt_required, get_jwt_identity)
from remanager_back.api.svg.servicios import crear_svg, editar_svg, borrar_svg, obtener_todos_los_svgs,\
    obtener_svg_por_id
from remanager_back.api.svg.serializadores import svg, svg_alta
from remanager_back.api.restplus import api

from remanager_back.data_auth.models import UserModel
from remanager_back.settings import AUTHORITY_ROOT

log = logging.getLogger(__name__)

ns = api.namespace('svgs', description='Servicios para manejar los svg de la aplicación, sólo para usuario ROOT')


@ns.route('/')
class Svg(Resource):

    @api.marshal_with(svg)
    @api.expect(svg_alta)
    @jwt_required
    def post(self):
        login = get_jwt_identity()
        current_user = UserModel.find_by_login(login)

        if not current_user.has_authority(AUTHORITY_ROOT):
            abort(401, 'No tiene permisos para realizar esta acción')

        data = request.data

        try:
            svg_obj = crear_svg(data)
            return svg_obj.to_dict()
        except Exception as exception:
            abort(500, 'Error del servidor al guardar el svg')

    @jwt_required
    def get(self):
        login = get_jwt_identity()
        current_user = UserModel.find_by_login(login)

        if not current_user.has_authority(AUTHORITY_ROOT):
            abort(401, 'No tiene permisos para realizar esta acción')

        try:
            svgs_objs = obtener_todos_los_svgs()

            svgs = [
                svg_obj.to_dict() for svg_obj in svgs_objs
            ]
            return svgs
        except Exception as exception:
            abort(500, 'Error del servidor al recuperar los svgs')


@ns.route('/<string:svg_id>')
class SvgById(Resource):

    @api.marshal_with(svg)
    @jwt_required
    def get(self, svg_id):
        login = get_jwt_identity()
        current_user = UserModel.find_by_login(login)

        try:
            svg_obj = obtener_svg_por_id(svg_id)

            if not svg_obj:
                abort(404, 'No existe un svg con ese id')
            return svg_obj.to_dict()
        except Exception as exception:
            abort(500, 'Error del servidor al recuperar el svg')

    @api.marshal_with(svg)
    @api.expect(svg)
    @jwt_required
    def put(self, svg_id):
        login = get_jwt_identity()
        current_user = UserModel.find_by_login(login)

        if not current_user.has_authority(AUTHORITY_ROOT):
            abort(401, 'No tiene permisos para realizar esta acción')

        data = request.data

        try:
            svg_obj = editar_svg(svg_id=svg_id, data=data)
            return svg_obj.to_dict()
        except Exception as exception:
            abort(500, 'Error del servidor al editar el svg')

    @jwt_required
    def delete(self, svg_id):
        login = get_jwt_identity()
        current_user = UserModel.find_by_login(login)

        if not current_user.has_authority(AUTHORITY_ROOT):
            abort(401, 'No tiene permisos para realizar esta acción')

        try:
            borrar_svg(svg_id)
            return {'message': 'svg borrado exitosamente'}
        except Exception as exception:
            abort(500, 'Error del servidor al borrar el svg')
