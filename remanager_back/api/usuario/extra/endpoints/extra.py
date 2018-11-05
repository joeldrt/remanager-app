import logging

from flask import request
from flask_restplus import Resource
from flask_jwt_extended import (jwt_required, get_jwt_identity)
from remanager_back.api.usuario.extra.servicios import create_user_extra, get_user_extra_by_login
from remanager_back.api.usuario.extra.serializadores import usuario_extra, fotos_extra, profile_picture
from remanager_back.api.restplus import api

log = logging.getLogger(__name__)

ns = api.namespace('usuario/extra', description='Servicios para manejar los datos extras del usuario')


@ns.route('/')
class GetUserExtra(Resource):

    @api.marshal_with(usuario_extra)
    @jwt_required
    def get(self):
        user_login = get_jwt_identity()

        try:
            extra = get_user_extra_by_login(user_login)
        except Exception as exception:
            extra = create_user_extra(user_login)

        return extra.to_dict()


@ns.route('/pictures')
class UpdateUserPictures(Resource):

    @api.expect(fotos_extra)
    @jwt_required
    def put(self):
        user_login = get_jwt_identity()

        try:
            extra = get_user_extra_by_login(user_login)
        except Exception as exception:
            extra = create_user_extra(user_login)

        data = request.json

        all_pictures_urls = data.get('picturesUrls')

        extra.picturesUrls = all_pictures_urls

        extra.save()

        return extra.to_dict()


@ns.route('/profile_picture')
class ProfilePicture(Resource):

    @api.expect(profile_picture)
    @jwt_required
    def put(self):
        user_login = get_jwt_identity()

        try:
            extra = get_user_extra_by_login(user_login)
        except Exception as exception:
            extra = create_user_extra(user_login)

        data = request.json

        profile_picture_url = data.get('profilePictureUrl')

        extra.profilePictureUrl = profile_picture_url

        extra.save()

        return extra.to_dict()
