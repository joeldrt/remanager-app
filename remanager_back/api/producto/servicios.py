from typing import List
from remanager_back.database.producto import Producto, ValorCampo
from mongoengine import Q


def crear_producto(organizacion_id: str, proyecto_id: str, correo_creador: str, id_seccion: str,
                   nombre: str, descripcion: str, precio: float, tipo_de_producto: str, estatus: str,
                   valores_campos: List[ValorCampo], fotos: List[str], archivos: List[str]) -> Producto:
    producto = Producto()
    producto.organizacionId = organizacion_id
    producto.proyectoId = proyecto_id
    producto.correoCreador = correo_creador
    producto.idSeccion = id_seccion
    producto.nombre = nombre
    producto.descripcion = descripcion
    producto.precio = precio
    producto.tipoDeProducto = tipo_de_producto
    producto.estatus = estatus

    producto.fotos = fotos
    producto.archivos = archivos

    for valor_campo_data in valores_campos:
        valor_campo = ValorCampo()
        valor_campo.nombre = valor_campo_data['nombre']
        valor_campo.valor = valor_campo_data['valor']
        valor_campo.icono = valor_campo_data['icono']
        valor_campo.tipoCampo = valor_campo_data['tipoCampo']
        producto.valoresCampos.append(valor_campo)

    producto.save()

    return producto


def obtener_productos() -> List[Producto]:
    productos = Producto.objects()
    return productos


def obtener_productos_por_proyecto_id(proyecto_id: str) -> List[Producto]:
    productos = Producto.objects(proyectoId=proyecto_id)
    return productos


def obtener_productos_por_organizacion_id(organizacion_id: str) -> List[Producto]:
    productos = Producto.objects(organizacionId=organizacion_id)
    return productos


def obtener_productos_por_organizacion_id_y_proyecto_id(organizacion_id: str, proyecto_id: str) -> List[Producto]:
    productos = Producto.objects(Q(organizacionId=organizacion_id) &
                                 Q(proyectoId=proyecto_id))
    return productos


def obtener_producto_por_id(producto_id: str) -> Producto:
    producto = Producto.objects(id=producto_id).first()
    return producto


def obtener_producto_por_id_y_organizacion_id(producto_id: str, organizacion_id: str) -> Producto:
    producto = Producto.objects(Q(id=producto_id) &
                                Q(organizacionId=organizacion_id)).first()
    return producto


def editar_producto(producto_id: str, organizacion_id: str, proyecto_id: str, correo_creador: str, id_seccion: str,
                    nombre: str, descripcion: str, precio: float, tipo_de_producto: str, estatus: str,
                    valores_campos: List[ValorCampo], fotos: List[str], archivos: List[str]) -> Producto:
    producto = obtener_producto_por_id(producto_id)
    producto.organizacionId = organizacion_id
    producto.proyectoId = proyecto_id
    producto.correoCreador = correo_creador
    producto.idSeccion = id_seccion
    producto.nombre = nombre
    producto.descripcion = descripcion
    producto.precio = precio
    producto.tipoDeProducto = tipo_de_producto
    producto.estatus = estatus

    producto.fotos = fotos
    producto.archivos = archivos

    temp_valores_campos = list(producto.valoresCampos)
    for valor_campo in temp_valores_campos:
        producto.valoresCampos.remove(valor_campo)

    for valor_campo_data in valores_campos:
        valor_campo = ValorCampo()
        valor_campo.nombre = valor_campo_data['nombre']
        valor_campo.valor = valor_campo_data['valor']
        valor_campo.icono = valor_campo_data['icono']
        valor_campo.tipoCampo = valor_campo_data['tipoCampo']
        producto.valoresCampos.append(valor_campo)

    producto.save()

    return producto


def borrar_producto_por_id(producto_id: str):
    producto = obtener_producto_por_id(producto_id=producto_id)
    producto.delete()


def actualizar_estatus_del_producto(producto_id: str, estatus: str):
    producto = Producto.objects.get(id=producto_id)
    producto.estatus = estatus
    producto.save()


