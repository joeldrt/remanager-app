import logging
import os
import base64

from flask import request
from flask_restplus import Resource
from flask_jwt_extended import (jwt_required)
from remanager_back.api.archivos.serializadores import envio_archivos
from remanager_back.api.restplus import api
from remanager_back.settings import WEB_FOLDER_NAME

log = logging.getLogger(__name__)

ns = api.namespace('file/upload', description='Servicios para manejar archivos')


@ns.route('/')
class Archivos(Resource):

    @api.expect(envio_archivos)
    @jwt_required
    def post(self):
        data = request.json

        folder = data.get('folder').replace(" ", "_")
        files = list(data.get('files'))

        if len(files) <= 0:
            return {'message', 'No files in request'}, 400

        added_files = []

        for current_file in files:
            os.makedirs('static/{}'.format(folder), exist_ok=True)

            base64_data = str(current_file['value'])

            filename = current_file['filename'].replace(" ", "_")

            saving_file = open('static/{}/{}'.format(folder, filename), 'wb')
            saving_file.write(base64.decodebytes(base64_data.encode()))
            saving_file.close()

            saved_file_name = '{}/{}/{}'.format(WEB_FOLDER_NAME, folder, filename)

            added_files.append(saved_file_name)

        return added_files
