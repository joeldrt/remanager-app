from typing import List
from mongoengine import Q
import datetime

from remanager_back.database.proyecto import Proyecto


def obtener_proyectos_por_organizacion(organizacion_id: str) -> List[Proyecto]:
    proyectos = Proyecto.objects(organizacionId=organizacion_id)
    return proyectos


def obtener_proyectos_root_por_organizacion(organizacion_id: str) -> List[Proyecto]:
    proyectos = Proyecto.objects(Q(organizacionId=organizacion_id) &
                                 Q(padreId='root'))
    return proyectos


def obtener_proyectos_por_padreId(organizacion_id: str, padre_id: str) -> List[Proyecto]:
    proyectos = Proyecto.objects(Q(organizacionId=organizacion_id) &
                                 Q(padreId=padre_id))
    return proyectos


def obtener_productos_por_id_seccion(organizacion_id: str, id_seccion: str) -> List[Proyecto]:
    proyectos = Proyecto.objects(Q(organizacionId=organizacion_id) &
                                 Q(idSeccion=id_seccion))
    return proyectos


def obtener_proyecto_por_id(organizacion_id: str, proyecto_id: str) -> Proyecto:
    proyecto = Proyecto.objects(Q(organizacionId=organizacion_id) &
                                Q(id=proyecto_id)).first()
    return proyecto


def root_obtener_todos_los_proyectos() -> List[Proyecto]:
    proyectos = [
        proyecto.to_dict() for proyecto in Proyecto.objects().all()
    ]
    return proyectos
