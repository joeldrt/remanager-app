from typing import List

from remanager_back.data_auth.models import UserModel, AuthorityModel


def crear_usuario(login: str, password: str, first_name: str, last_name: str, email: str,
                  organization_id: str, authorities: List[str]) -> UserModel:

    user = UserModel(
        login=login,
        password=UserModel.generate_hash(password),
        firstName=first_name,
        lastName=last_name,
        email=email,
        organizationId=organization_id,
        activated=False
    )

    for authority_str in authorities:
        authority = AuthorityModel.find_by_authority_name(authority_str)
        if authority is not None:
            user.authorities.append(authority)

    user.save_to_db()

    return user


def obtener_usuarios_por_organizacion_id(organizacion_id: str) -> List[UserModel]:
    usuarios = UserModel.find_by_organization_id(organizacion_id)
    return usuarios


def obtener_usuarios_todos(organizacion_id: str) -> List[UserModel]:
    usuarios = UserModel.find_by_organizacion_all(organizacion_id)
    return usuarios


def editar_usuario(id: int, first_name: str, last_name: str, organization_id: str, authorities: List[str]) -> UserModel:
    user = UserModel.find_by_id(id)

    requested_authorities = []

    for authority_str in authorities:
        authority = AuthorityModel.find_by_authority_name(authority_str)
        if authority is not None:
            requested_authorities.append(authority)

    user.firstName = first_name
    user.lastName = last_name
    user.organizationId = organization_id

    # se quitan las categorias que el usuario pueda tener y que no vengan en las categorias solicitadas
    for authority in user.authorities:
        if authority not in requested_authorities:
            user.authorities.remove(authority)

    # se agregan las categorias nuevas que no tenga ya el usuario pero que vengan en la solicitud
    for authority in requested_authorities:
        if authority not in user.authorities:
            user.authorities.append(authority)

    user.save_to_db()

    return user


def borrar_usuario(id: int):
    user = UserModel.find_by_id(id)
    user.delete_me()
