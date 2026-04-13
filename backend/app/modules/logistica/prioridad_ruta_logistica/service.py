from app.modules.logistica.prioridad_ruta_logistica.repository import (
    consultar_todas_las_prioridades_ruta_logistica_en_bd,
)
from app.modules.logistica.prioridad_ruta_logistica.schema import (
    convertir_prioridad_ruta_logistica_a_respuesta,
)


def listar_prioridades_ruta_logistica_para_respuesta():
    """Consulta el catalogo de prioridades de rutas logisticas."""
    prioridades = consultar_todas_las_prioridades_ruta_logistica_en_bd()
    return [
        convertir_prioridad_ruta_logistica_a_respuesta(prioridad)
        for prioridad in prioridades
    ]
