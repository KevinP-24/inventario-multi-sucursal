from app.extensions import db
from app.modules.logistica.prioridad_ruta_logistica.model import PrioridadRutaLogistica
from app.modules.logistica.ruta_logistica.model import RutaLogistica


def consultar_todas_las_rutas_logistica_en_bd():
    """Consulta en PostgreSQL todas las rutas logisticas ordenadas por nombre."""
    return RutaLogistica.query.order_by(RutaLogistica.nombre_ruta.asc()).all()


def consultar_rutas_logistica_clasificadas_en_bd(criterio):
    """Consulta rutas ordenadas por prioridad, costo o tiempo estimado."""
    if criterio == "prioridad":
        prioridad_orden = db.case(
            (PrioridadRutaLogistica.nombre == "URGENTE", 1),
            (PrioridadRutaLogistica.nombre == "ALTA", 2),
            (PrioridadRutaLogistica.nombre == "NORMAL", 3),
            (PrioridadRutaLogistica.nombre == "BAJA", 4),
            else_=5,
        )
        return (
            RutaLogistica.query
            .join(
                PrioridadRutaLogistica,
                RutaLogistica.id_prioridad_ruta == PrioridadRutaLogistica.id_prioridad_ruta,
            )
            .order_by(prioridad_orden, RutaLogistica.nombre_ruta.asc())
            .all()
        )

    if criterio == "costo":
        return RutaLogistica.query.order_by(
            RutaLogistica.costo_estimado.asc(),
            RutaLogistica.nombre_ruta.asc(),
        ).all()

    return RutaLogistica.query.order_by(
        RutaLogistica.tiempo_estimado.asc(),
        RutaLogistica.nombre_ruta.asc(),
    ).all()


def consultar_ruta_logistica_por_id_en_bd(id_ruta):
    """Consulta en PostgreSQL una ruta logistica usando su id."""
    return RutaLogistica.query.get(id_ruta)


def consultar_ruta_logistica_por_nombre_en_bd(nombre_ruta):
    """Consulta si ya existe una ruta logistica con ese nombre."""
    return RutaLogistica.query.filter_by(nombre_ruta=nombre_ruta).first()


def consultar_cumplimiento_logistico_en_bd(id_sucursal=None, id_ruta=None):
    """Consulta envios con transferencia y ruta para calcular cumplimiento."""
    from app.modules.logistica.envio_transferencia.model import EnvioTransferencia
    from app.modules.transferencias.transferencia.model import Transferencia

    consulta = (
        EnvioTransferencia.query
        .join(Transferencia, EnvioTransferencia.id_transferencia == Transferencia.id_transferencia)
        .join(RutaLogistica, EnvioTransferencia.id_ruta == RutaLogistica.id_ruta)
    )

    if id_sucursal:
        consulta = consulta.filter(
            (Transferencia.id_sucursal_origen == id_sucursal)
            | (Transferencia.id_sucursal_destino == id_sucursal)
        )

    if id_ruta:
        consulta = consulta.filter(EnvioTransferencia.id_ruta == id_ruta)

    return consulta.order_by(EnvioTransferencia.fecha_envio.desc()).all()


def guardar_ruta_logistica_en_base_de_datos(ruta_logistica):
    """Inserta o actualiza una ruta logistica en PostgreSQL."""
    db.session.add(ruta_logistica)
    db.session.commit()
    return ruta_logistica
