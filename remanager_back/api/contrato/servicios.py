from typing import List
from datetime import datetime, timedelta
from passlib.hash import pbkdf2_sha256 as sha256

from mongoengine import Q

from remanager_back.database.contrato import Contrato, PagoProgramado, PagoReal
from remanager_back.api.producto.servicios import obtener_producto_por_id, actualizar_estatus_del_producto
from remanager_back.api.cliente.servicios import obtener_cliente_por_id

import json


def crear_contrato(tipo: str, cliente_id: str, producto_id: str, correo_vendedor: str, dias_validez: int,
                   pagos_programados: List[PagoProgramado]) -> Contrato:
    contrato = Contrato()
    contrato.tipo = tipo
    contrato.clienteId = cliente_id
    contrato.productoId = producto_id
    contrato.correoVendedor = correo_vendedor
    contrato.diasValidez = -1 if not dias_validez else dias_validez

    pagos_programados_objs = []

    if pagos_programados:
        for pago_programado_dict in pagos_programados:
            pago_programado_obj = PagoProgramado()
            pago_programado_obj.fechaCompromisoPago = pago_programado_dict['fechaCompromisoPago']
            pago_programado_obj.monto = pago_programado_dict['monto']
            pagos_programados_objs.append(pago_programado_obj)

    if len(pagos_programados_objs) > 0:
        formatear_pagos_programados(pagos_programados=pagos_programados_objs)
        contrato.pagosProgramados = pagos_programados_objs

    contrato.save()

    producto = obtener_producto_por_id(producto_id=producto_id)

    if not producto:
        contrato.delete()
        raise Exception('No se encontró el producto - se destruye el contrato')

    if not contrato.tipo == 'CORRIDA':
        producto.estatus = map_estatus_tipo_de_contrato(contrato.tipo)
        producto.save()

    return contrato


def obtener_contratos() -> List[Contrato]:
    contratos = Contrato.objects()
    return contratos


def obtener_contratos_por_correo_vendedor(correo_vendedor: str) -> List[Contrato]:
    contratos = Contrato.objects(correoVendedor=correo_vendedor)
    return contratos


def obtener_contratos_por_cliente_id(cliente_id: str) -> List[Contrato]:
    contratos = Contrato.objects(Q(activo=True) &
                                 Q(clienteId=cliente_id)).all()
    return contratos


def obtener_resumen_contratos_por_cliente(cliente_id: str) -> dict:
    resumen = dict()

    contratos_objs = obtener_contratos_por_cliente_id(cliente_id=cliente_id)

    resumen['cliente'] = obtener_cliente_por_id(cliente_id=cliente_id).to_dict()

    lista_contratos_con_producto = []

    for contrato_obj in contratos_objs:
        entrada_contrato_con_producto = dict()
        entrada_contrato_con_producto['contrato'] = contrato_obj.to_dict()
        producto_obj = obtener_producto_por_id(producto_id=contrato_obj.productoId)
        entrada_contrato_con_producto['producto'] = producto_obj.to_dict()
        lista_contratos_con_producto.append(entrada_contrato_con_producto)

    resumen['resumen_contratos'] = lista_contratos_con_producto

    return resumen


def obtener_contrato_por_contrato_id(contrato_id: str) -> Contrato:
    contrato = Contrato.objects(id=contrato_id).first()
    return contrato


def obtener_contrato_por_contrato_id_y_correo_vendedor(contrato_id: str, correo_vendedor: str) -> Contrato:
    contrato = Contrato.objects(Q(id=contrato_id) &
                                Q(correoVendedor=correo_vendedor)).first()
    return contrato


def obtener_contratos_por_producto_id(producto_id: str) -> List[Contrato]:
    contratos = Contrato.objects(productoId=producto_id).all()
    return contratos


def obtener_contratos_por_producto_id_y_correo_vendedor(producto_id: str, correo_vendedor: str) -> List[Contrato]:
    contratos = Contrato.objects(Q(productoId=producto_id) &
                                 Q(correoVendedor=correo_vendedor)).all()
    return contratos


def borrar_contrato(contrato_id: str):
    contrato = obtener_contrato_por_contrato_id(contrato_id=contrato_id)
    actualizar_estatus_del_producto(producto_id=contrato.productoId,
                                    estatus=map_estatus_tipo_de_contrato(tipo_de_contrato='CONTRATO_BORRADO'))
    contrato.delete()


def formatear_pagos_programados(pagos_programados: List[PagoProgramado]):
    for pago_programado in pagos_programados:
        pago_programado.fechaCompromisoPago = datetime.strptime(pago_programado.fechaCompromisoPago,
                                                                '%Y-%m-%dT%H:%M:%S.%fZ')
        pago_programado.uuid = sha256.hash('{}-{}-{}'.format(str(datetime.now()),
                                                             str(pago_programado.monto),
                                                             str(pago_programado.fechaCompromisoPago)))


def desactivar_contrato(contrato_id: str) -> Contrato:
    contrato = get_contrato_by_id(contrato_id=contrato_id)

    if int(contrato.diasValidez) > 0:
        fecha_creacion = contrato.fechaCreacion
        fecha_vencimiento = fecha_creacion + timedelta(days=int(contrato.diasValidez))
        if fecha_vencimiento > datetime.now():  # significa que sigue vigente el contrato
            producto = obtener_producto_por_id(contrato.productoId)
            producto.estatus = 'DISPONIBLE'
            producto.save()

    contrato.activo = False
    contrato.save()
    return contrato


def generar_objeto_pago_programado(fecha_compromiso_pago: datetime, monto: float) -> PagoProgramado:
    pago_programado = PagoProgramado()
    pago_programado.fechaCompromisoPago = fecha_compromiso_pago
    pago_programado.monto = monto

    return pago_programado


def agregar_pago_programado(contrato_id: str, pago_programado: PagoProgramado) -> Contrato:
    contrato = get_contrato_by_id(contrato_id)

    if not contrato:
        raise Exception('El contrato no se encontró')

    contrato.update(push__pagosProgramados=pago_programado)
    contrato.save()

    return contrato


def agregar_pago_real(contrato_id: str, data: json) -> Contrato:
    contrato = get_contrato_by_id(contrato_id)

    pago_real = PagoReal()
    pago_real.monto = data['monto']
    if 'archivos' in data.keys():
        pago_real.archivos = data['archivos']

    contrato.update(push__pagosReales=pago_real)
    contrato.save()

    return contrato


def map_estatus_tipo_de_contrato(tipo_de_contrato: str) -> str:
    switcher = {
        'CONTRATO_BORRADO': 'DISPONIBLE',
        'DEVOLUCION': 'DISPONIBLE',
        'BLOQUEO': 'BLOQUEADO',
        'APARTADO': 'APARTADO',
        'VENTA': 'VENDIDO'
    }
    return switcher.get(tipo_de_contrato)


def verify_cliente_exists(cliente_id: str) -> bool:
    if not cliente_id:
        return False
    try:
        cliente = obtener_cliente_por_id(cliente_id)
    except Exception:
        return False

    if not cliente:
        return False

    return True


def verify_producto_exists(producto_id: str) -> bool:
    if not producto_id:
        return False
    try:
        producto = obtener_producto_por_id(producto_id)
    except Exception:
        return False

    if not producto:
        return False

    return True


def find_all_contratos() -> List[Contrato]:
    contratos = Contrato.objects()
    return contratos


def get_last_contrato_for_producto_id(producto_id: str) -> Contrato:
    contrato = Contrato.objects(Q(activo=True) &
                                Q(producto_id=producto_id))[0]
    return contrato


def find_all_contratos_for_producto_id(producto_id: str) -> List[Contrato]:
    contratos = Contrato.objects(productoId=producto_id)
    return contratos


def get_contrato_by_id(contrato_id: str) -> Contrato:
    contrato = Contrato.objects(Q(activo=True) &
                                Q(id=contrato_id))[0]
    return contrato


def find_all_for_cliente_id(cliente_id: str) -> List[Contrato]:
    contratos = Contrato.objects(Q(activo=True) &
                                 Q(clienteId=cliente_id))
    return contratos

