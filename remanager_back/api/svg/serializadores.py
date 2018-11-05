from flask_restplus import fields
from remanager_back.api.restplus import api

punto = api.model('Punto', {
    'x': fields.Float(description='coordenada x para el punto'),
    'y': fields.Float(description='coordenada y para el punto')
})

poligono = api.model('Poligono', {
    'puntos': fields.String(description='puntos del poligono'),
    'genUid': fields.String(description='uuid del poligono, para relacionar un producto o proyecto'),
    'arregloPuntos': fields.List(fields.Nested(punto))
})

svg = api.model('Svg', {
    'fechaAlta': fields.DateTime(description='fecha de creacion del svg'),
    'nombre': fields.String(description='nombre del svg'),
    'imagenContentType': fields.String(description='tipo de contenido de la imagen del svg'),
    'imagen': fields.String(description='imagen en base 64'),
    'width': fields.String(description='ancho del svg'),
    'height': fields.String(description='alto del svg'),
    'codigoContentType': fields.String(description='tipo del codigo del svg completo en base 64'),
    'codigo': fields.String(description='svg completo en base 64'),
    'proyectoId': fields.String(description='Id del proyecto al que pertenecen'),
    'poligonos': fields.List(fields.Nested(poligono))
})
