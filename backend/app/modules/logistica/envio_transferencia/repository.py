from app.extensions import db
from app.modules.logistica.envio_transferencia.model import EnvioTransferencia


def consultar_envio_por_transferencia_en_bd(id_transferencia):
    """Consulta el envio asociado a una transferencia."""
    return EnvioTransferencia.query.filter_by(id_transferencia=id_transferencia).first()


def guardar_envio_transferencia_en_base_de_datos(envio):
    """Inserta o actualiza un envio de transferencia."""
    db.session.add(envio)
    db.session.commit()
    return envio
