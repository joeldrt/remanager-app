from typing import List
import json

from remanager_back.database.svg import Svg


def crear_svg(data: json) -> Svg:
    svg = Svg.from_json(data)
    svg.save()
    return svg


def editar_svg(svg_id: str, data: json) -> Svg:
    svg = obtener_svg_por_id(svg_id)
    if svg.id != data['id']:
        raise Exception('Diferentes Objetos')

    svg = Svg.from_json(data)
    svg.save()
    return svg


def borrar_svg(svg_id: str) -> Svg:
    svg = obtener_svg_por_id(svg_id)
    svg.delete()


def obtener_todos_los_svgs() -> List[Svg]:
    svg = Svg.objects().all
    return svg


def obtener_svg_por_id(svg_id: str) -> Svg:
    svg = Svg.objects(id=svg_id).first()
    return svg