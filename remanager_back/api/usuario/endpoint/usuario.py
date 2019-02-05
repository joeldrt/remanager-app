import logging

from flask import request
from flask_restplus import Resource, reqparse, abort
from flask_jwt_extended import (jwt_required, get_jwt_identity)
from remanager_back.api.usuario.servicios import crear_usuario, obtener_usuarios_por_organizacion_id, editar_usuario,\
    borrar_usuario, obtener_usuarios_todos
from remanager_back.api.usuario.serializadores import usuario, usuario_alta, usuario_editar
from remanager_back.api.restplus import api

from remanager_back.data_auth.models import UserModel

from remanager_back.settings import MINIMUM_USER_API_AUTHORITY, AUTHORITY_ROOT, ROOT_OBJECT

log = logging.getLogger(__name__)

ns = api.namespace('usuarios', description='Servicios para manejar a los usuarios')


@ns.route('/')
class User(Resource):

    @api.marshal_with(usuario)
    @api.expect(usuario_alta)
    @jwt_required
    def post(self):
        login = get_jwt_identity()
        current_user = UserModel.find_by_login(login)

        if not current_user.has_authority(MINIMUM_USER_API_AUTHORITY):
            abort(401, 'No tiene permisos para realizar esta acción')

        data = request.json

        if UserModel.find_by_login(data.get('login')):
            abort(400, 'Ya existe un usuario con ese sobrenombre')

        if UserModel.find_by_email(data.get('email')):
            abort(400, 'Ya existe un usuario con ese email')

        for authority_str in data.get('authorities'):
            if not current_user.has_authority(authority_str):
                abort(401, 'No se pueden asignar autoridades para el usuario con las que el solicitante no cuenta')

        try:
            user = crear_usuario(login=data.get('login'), password=data.get('password'), first_name=data.get('firstName'),
                                 last_name=data.get('lastName'), email=data.get('email'),
                                 organization_id=data.get('organizationId'), authorities=data.get('authorities'))
            return user.to_json()
        except Exception as exception:
            abort(500, 'Error del servidor al guardar el usuario')

    @api.marshal_list_with(usuario)
    @jwt_required
    def get(self):
        login = get_jwt_identity()
        current_user = UserModel.find_by_login(login)

        if not current_user.has_authority(MINIMUM_USER_API_AUTHORITY):
            abort(401, 'No tiene permisos para realizar esta acción')

        if current_user.has_authority(AUTHORITY_ROOT):
            usuarios_obj = obtener_usuarios_todos(organizacion_id=current_user.organizationId)
        else:
            usuarios_obj = obtener_usuarios_por_organizacion_id(organizacion_id=current_user.organizationId)
        usuarios = [
            usuario.to_json() for usuario in usuarios_obj
        ]
        return usuarios


@ns.route('/<string:usuario_id>')
class UserActions(Resource):

    @api.marshal_with(usuario)
    @api.expect(usuario_editar)
    @jwt_required
    def put(self, usuario_id):
        login = get_jwt_identity()
        current_user = UserModel.find_by_login(login)

        if not current_user.has_authority(MINIMUM_USER_API_AUTHORITY):
            abort(401, 'No tiene permisos para realizar esta acción')

        data = request.json

        if int(usuario_id) != data.get('id'):
            abort(400, 'No coinciden los ids del usuario')

        for authority_str in data.get('authorities'):
            if not current_user.has_authority(authority_str):
                abort(401, 'No se pueden asignar autoridades para el usuario con las que el solicitante no cuenta')

        try:
            user = editar_usuario(id=usuario_id,
                                  first_name=data.get('firstName'),
                                  last_name=data.get('lastName'),
                                  organization_id=data.get('organizationId'),
                                  authorities=data.get('authorities'))
            return user.to_json()
        except Exception as exception:
            abort(500, 'Error del servidor al editar el usuario')

    @jwt_required
    def delete(self, usuario_id):
        login = get_jwt_identity()
        current_user = UserModel.find_by_login(login)

        if not current_user.has_authority(MINIMUM_USER_API_AUTHORITY):
            abort(401, 'No tiene permisos para realizar esta acción')

        if usuario_id == current_user.id:
            abort(401, 'No se puede borrar a si mismo')

        if not UserModel.find_by_id(usuario_id):
            abort(401, 'No existe el usuario con ese id')

        if not current_user.has_authority(AUTHORITY_ROOT) and UserModel.find_by_id(usuario_id).login == ROOT_OBJECT['login']:
            abort(403, 'No tienes permisos para ver este usuario')

        try:
            borrar_usuario(usuario_id)
        except Exception as exception:
            abort(500, 'Error del servidor al borrar el usuario')

        return {'message': 'Se borró correctamente el usuario con el id: {}'.format(usuario_id)}

    @api.marshal_with(usuario)
    @jwt_required
    def get(self, usuario_id):
        login = get_jwt_identity()
        current_user = UserModel.find_by_login(login)

        if not current_user.has_authority(MINIMUM_USER_API_AUTHORITY):
            abort(401, 'No tiene permisos para realizar esta acción')

        user = UserModel.find_by_id(usuario_id)

        if not user:
            abort(401, 'No existe el usuario con ese id')

        if not current_user.has_authority(AUTHORITY_ROOT) and user.login == ROOT_OBJECT['login']:
            abort(403, 'No tienes permisos para ver este usuario')

        return user.to_json()


change_pss_parser = reqparse.RequestParser(bundle_errors=True)
change_pss_parser.add_argument('new_password', required=True, type=str)


@ns.route('/<string:usuario_id>/password')
class ChangeUserPassword(Resource):

    @api.expect(change_pss_parser)
    @jwt_required
    def put(self, usuario_id):
        login = get_jwt_identity()
        current_user = UserModel.find_by_login(login)

        if not current_user.has_authority(MINIMUM_USER_API_AUTHORITY):
            abort(401, 'No tiene permisos para realizar esta acción')

        user = UserModel.find_by_id(usuario_id)

        if not user:
            abort(401, 'No existe el usuario con ese id')

        if not current_user.has_authority(AUTHORITY_ROOT) and user.login == ROOT_OBJECT['login']:
            abort(403, 'No tienes permisos para editar este usuario')

        data = change_pss_parser.parse_args()

        user.password = UserModel.generate_hash(data['new_password'])

        user.save_to_db()

        return {'message': 'El password se ha cambiado correctamente'}


change_activated_status_parser = reqparse.RequestParser(bundle_errors=True)
change_activated_status_parser.add_argument('status', required=True, type=bool)


@ns.route('/<string:usuario_id>/activated')
class ChangeUserActivateStatus(Resource):

    @api.expect(change_activated_status_parser)
    @jwt_required
    def put(self, usuario_id):
        login = get_jwt_identity()
        current_user = UserModel.find_by_login(login)

        if not current_user.has_authority(AUTHORITY_ROOT):
            abort(401, 'No tiene permisos para realizar esta acción')

        user = UserModel.find_by_id(usuario_id)

        if not user:
            abort(401, 'No existe el usuario con ese id')

        if user.login == current_user.login:
            abort(404, 'No puedes modificar tu propio estado')

        data = change_activated_status_parser.parse_args()

        user.activated = data['status']

        user.save_to_db()

        return {'message': 'se ha cambiado el estado del usuario: {} a activado={}'.format(user.login, user.activated)}
