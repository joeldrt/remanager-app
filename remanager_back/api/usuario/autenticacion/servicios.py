from typing import List

from remanager_back.database.organizacion import Organizacion


def obtener_todas_las_organizaciones() -> List[Organizacion]:
    organizacion = [
        organizacion.to_dict() for organizacion in Organizacion.objects().all()
    ]
    return organizacion


def obtener_organizacion_por_id(organizacion_id: str) -> Organizacion:
    organizacion = Organizacion.objects().get(id=organizacion_id)
    return organizacion