import logging
import traceback

from flask_restplus import Api
from remanager_back import settings
from sqlalchemy.orm.exc import NoResultFound

log = logging.getLogger(__name__)

authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}
api = Api(version='1.0', title='Real State Manager API',
          description='Backend para administración de bienes raices creado por Digiall',
          authorizations=authorizations,
          security='apikey')


@api.errorhandler
def default_error_handler(e):
    message = 'Ha ocurrido una excepción sin manejar'
    log.exception(message)

    if not settings.FLASK_DEBUG:
        return {'message': message}, 500


@api.errorhandler(NoResultFound)
def database_not_found_error_handler(e):
    log.warning(traceback.format_exc())
    return {'message': 'No se pudo encontrar la base de datos'}, 404
