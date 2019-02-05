from typing import List
import json

from remanager_back.database.svg import Svg


def crear_svg(data: json) -> Svg:
    svg = Svg.from_json(data)
    svg.save()
    return svg


def editar_svg(svg_id: str, data: json) -> Svg:
    svg = obtener_svg_por_id(svg_id)
    new_svg = Svg.from_json(data)
    svg.fechaAlta = new_svg.fechaAlta
    svg.nombre = new_svg.nombre
    svg.imagenContentType = new_svg.imagenContentType
    svg.imagen = new_svg.imagen
    svg.width = new_svg.width
    svg.height = new_svg.height
    svg.codigoContentType = new_svg.codigoContentType
    svg.codigo = new_svg.codigo
    svg.poligonos = new_svg.poligonos
    svg.save()
    return svg


def borrar_svg(svg_id: str) -> Svg:
    svg = obtener_svg_por_id(svg_id)
    svg.delete()


def obtener_todos_los_svgs() -> List[Svg]:
    svg = Svg.objects().all()
    return svg


def obtener_svg_por_id(svg_id: str) -> Svg:
    svg = Svg.objects(id=svg_id).first()
    return svg