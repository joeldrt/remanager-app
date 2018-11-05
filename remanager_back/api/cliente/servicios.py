from typing import List
from datetime import datetime
from mongoengine import Q

from remanager_back.database.cliente import Cliente


def crear_cliente(organizacion_id: str, correo_vendedor: str, nombre: str, apellidos: str, direccion: str,
                  fecha_nacimiento: datetime, telefono: str, email: str) -> Cliente:

    cliente = Cliente()
    cliente.organizacionId = organizacion_id
    cliente.correoVendedor = correo_vendedor
    cliente.nombre = nombre
    cliente.apellidos = apellidos
    cliente.direccion = direccion
    cliente.fechaNacimiento = fecha_nacimiento
    cliente.telefono = telefono
    cliente.email = email

    cliente.save()

    return cliente


def editar_cliente(cliente_id: str, email: str, nombre: str, apellidos: str, fecha_nacimiento: datetime,
                   direccion: str, telefono: str) -> Cliente:

    cliente = obtener_cliente_por_id(cliente_id=cliente_id)
    cliente.email = email
    cliente.nombre = nombre
    cliente.apellidos = apellidos
    cliente.fechaNacimiento = fecha_nacimiento
    cliente.direccion = direccion
    cliente.telefono = telefono

    cliente.save()

    return cliente


def obtener_cliente_por_id_correo_vendedor(correo_vendedor: str, cliente_id: str) -> Cliente:
    cliente = Cliente.objects(Q(correoVendedor=correo_vendedor) &
                              Q(id=cliente_id)).first()
    return cliente


def obtener_cliente_por_id(cliente_id: str) -> Cliente:
    cliente = Cliente.objects(id=cliente_id).first()
    return cliente


def borrar_cliente_por_id(cliente_id: str) -> bool:
    cliente = Cliente.objects(id=cliente_id).first()
    cliente.delete()
    return True


def obtener_todos_los_clientes_por_organizacion_id(organizacion_id: str) -> List[Cliente]:
    clientes = Cliente.objects(organizacionId=organizacion_id)
    return clientes


def obtener_clientes_por_correo_vendedor(correo_vendedor: str) -> List[Cliente]:
    clientes = Cliente.objects(correoVendedor=correo_vendedor)
    return clientes


def root_obtener_todos_los_clientes() -> List[Cliente]:
    clientes = Cliente.objects().all()
    return clientes
