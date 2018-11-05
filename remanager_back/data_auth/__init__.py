from flask_sqlalchemy import SQLAlchemy
from remanager_back import settings
from remanager_back.database import global_init as mongo_init

db = SQLAlchemy()


def reset_database():
    from remanager_back.data_auth.models import UserModel, AuthorityModel, RevokedTokenModel
    db.drop_all()
    db.create_all()

    if not UserModel.find_by_login('admin'):
        mongo_init()
        init_database_values()


def init_database_values():
    from remanager_back.data_auth.models import UserModel, AuthorityModel, RevokedTokenModel
    from remanager_back.database.organizacion import Organizacion

    authority0 = AuthorityModel(authority_name=settings.AUTHORITY_ROOT)
    authority0.save_to_db()
    authority1 = AuthorityModel(authority_name=settings.AUTHORITY_ADMIN)
    authority1.save_to_db()
    authority2 = AuthorityModel(authority_name=settings.AUTHORITY_USER)
    authority2.save_to_db()

    root = UserModel(
        login=settings.ROOT_OBJECT['login'],
        password=UserModel.generate_hash(settings.ROOT_OBJECT['password']),
        firstName=settings.ROOT_OBJECT['firstName'],
        email=settings.ROOT_OBJECT['email'],
        activated=True
    )

    root.authorities.append(authority0)
    root.authorities.append(authority1)
    root.authorities.append(authority2)

    root.save_to_db()

    admin = UserModel(
        login=settings.ADMIN_OBJECT['login'],
        password=UserModel.generate_hash(settings.ADMIN_OBJECT['password']),
        firstName=settings.ADMIN_OBJECT['firstName'],
        lastName=settings.ADMIN_OBJECT['lastName'],
        email=settings.ADMIN_OBJECT['email'],
        activated=True
    )

    admin.authorities.append(authority1)
    admin.authorities.append(authority2)

    admin.save_to_db()

    organizacion = Organizacion.objects(correoCreador=settings.ORGANIZACION_OBJECT['correo_creador']).first()

    if organizacion is None:
        organizacion = Organizacion()
        organizacion.nombre = settings.ORGANIZACION_OBJECT['nombre']
        organizacion.descripcion = settings.ORGANIZACION_OBJECT['descripcion']
        organizacion.correoCreador = settings.ORGANIZACION_OBJECT['correo_creador']
        organizacion.save()

    root.organizationId = str(organizacion.id)
    root.save_to_db()

    admin.organizationId = str(organizacion.id)
    admin.save_to_db()

