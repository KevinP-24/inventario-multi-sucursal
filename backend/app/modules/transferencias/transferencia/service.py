from datetime import datetime

from app.extensions import db
from app.modules.auth.usuario.repository import consultar_usuario_por_id_en_bd
from app.modules.inventario.inventario_sucursal.model import InventarioSucursal
from app.modules.inventario.inventario_sucursal.repository import (
    consultar_inventario_por_sucursal_y_producto_en_bd,
)
from app.modules.inventario.movimiento_inventario.model import MovimientoInventario
from app.modules.inventario.producto.repository import consultar_producto_por_id_en_bd
from app.modules.inventario.producto_unidad.repository import consultar_producto_unidad_por_id_en_bd
from app.modules.inventario.tipo_movimiento_inventario.repository import (
    consultar_tipo_movimiento_inventario_por_nombre_en_bd,
)
from app.modules.logistica.envio_transferencia.model import EnvioTransferencia
from app.modules.logistica.envio_transferencia.repository import (
    consultar_envio_por_transferencia_en_bd,
)
from app.modules.logistica.envio_transferencia.schema import (
    convertir_envio_transferencia_a_respuesta,
    convertir_texto_a_fecha_hora,
    validar_datos_para_registrar_envio_transferencia,
)
from app.modules.logistica.ruta_logistica.repository import consultar_ruta_logistica_por_id_en_bd
from app.modules.logistica.transportista.repository import consultar_transportista_por_id_en_bd
from app.modules.sucursales.sucursal.repository import consultar_sucursal_por_id_en_bd
from app.modules.transferencias.detalle_transferencia.model import DetalleTransferencia
from app.modules.transferencias.estado_transferencia.repository import (
    consultar_estado_transferencia_por_nombre_en_bd,
)
from app.modules.transferencias.incidencia_transferencia.model import IncidenciaTransferencia
from app.modules.transferencias.recepcion_transferencia.model import RecepcionTransferencia
from app.modules.transferencias.recepcion_transferencia.schema import (
    convertir_recepcion_transferencia_a_respuesta,
    convertir_valor_a_decimal as convertir_cantidad_recepcion,
    validar_datos_para_confirmar_recepcion_transferencia,
)
from app.modules.transferencias.transferencia.model import Transferencia
from app.modules.transferencias.transferencia.repository import (
    consultar_todas_las_transferencias_en_bd,
    consultar_transferencia_por_id_en_bd,
)
from app.modules.transferencias.transferencia.schema import (
    convertir_transferencia_a_respuesta,
    convertir_valor_a_decimal,
    validar_datos_para_crear_transferencia,
    validar_datos_para_revisar_transferencia,
)


def listar_transferencias_para_respuesta():
    """Consulta transferencias y las deja listas para API."""
    transferencias = consultar_todas_las_transferencias_en_bd()
    return [convertir_transferencia_a_respuesta(item) for item in transferencias]


def obtener_transferencia_para_respuesta(id_transferencia):
    """Consulta una transferencia por id y la deja lista para responder."""
    transferencia = consultar_transferencia_por_id_en_bd(id_transferencia)
    if not transferencia:
        return None

    return convertir_transferencia_a_respuesta(transferencia)


def crear_transferencia_con_validaciones(datos):
    """Registra la solicitud formal de transferencia entre sucursales."""
    errores = validar_datos_para_crear_transferencia(datos)
    if errores:
        return None, errores

    errores_relaciones = validar_relaciones_de_solicitud(datos)
    if errores_relaciones:
        return None, errores_relaciones

    estado_solicitada = obtener_estado_transferencia("SOLICITADA")
    if not estado_solicitada:
        return None, {"estado_transferencia": "No existe el estado SOLICITADA."}

    detalles = construir_detalles_de_solicitud(datos["detalles"])

    transferencia = Transferencia(
        id_sucursal_origen=datos["id_sucursal_origen"],
        id_sucursal_destino=datos["id_sucursal_destino"],
        id_usuario_solicita=datos["id_usuario_solicita"],
        id_estado_transferencia=estado_solicitada.id_estado_transferencia,
        prioridad=(datos.get("prioridad") or "NORMAL").strip().upper(),
        observacion=(datos.get("observacion") or "").strip() or None,
        detalles=detalles,
    )

    db.session.add(transferencia)
    db.session.commit()
    return convertir_transferencia_a_respuesta(transferencia), None


def revisar_transferencia_con_validaciones(id_transferencia, datos):
    """Permite a la sucursal origen aprobar, ajustar o rechazar la solicitud."""
    errores = validar_datos_para_revisar_transferencia(datos)
    if errores:
        return None, errores

    transferencia = consultar_transferencia_por_id_en_bd(id_transferencia)
    if not transferencia:
        return None, {"transferencia": "No existe una transferencia con ese id."}

    if obtener_nombre_estado(transferencia) != "SOLICITADA":
        return None, {"estado": "Solo se pueden revisar transferencias en estado SOLICITADA."}

    accion = (datos.get("accion") or "").strip().upper()
    if accion == "RECHAZAR":
        estado_rechazada = obtener_estado_transferencia("RECHAZADA")
        transferencia.id_estado_transferencia = estado_rechazada.id_estado_transferencia
        transferencia.observacion = (datos.get("observacion") or transferencia.observacion)
        db.session.commit()
        return convertir_transferencia_a_respuesta(transferencia), None

    errores_aprobacion = aplicar_cantidades_aprobadas(transferencia, datos["detalles"])
    if errores_aprobacion:
        return None, errores_aprobacion

    estado_aprobada = obtener_estado_transferencia("APROBADA")
    transferencia.id_estado_transferencia = estado_aprobada.id_estado_transferencia
    transferencia.observacion = (datos.get("observacion") or transferencia.observacion)
    db.session.commit()
    return convertir_transferencia_a_respuesta(transferencia), None


def registrar_envio_transferencia_con_validaciones(id_transferencia, datos):
    """Registra el despacho y descuenta el inventario de la sucursal origen."""
    errores = validar_datos_para_registrar_envio_transferencia(datos)
    if errores:
        return None, None, errores

    transferencia = consultar_transferencia_por_id_en_bd(id_transferencia)
    if not transferencia:
        return None, None, {"transferencia": "No existe una transferencia con ese id."}

    if obtener_nombre_estado(transferencia) != "APROBADA":
        return None, None, {"estado": "Solo se pueden enviar transferencias APROBADAS."}

    if consultar_envio_por_transferencia_en_bd(id_transferencia):
        return None, None, {"envio": "La transferencia ya tiene un envio registrado."}

    if not consultar_ruta_logistica_por_id_en_bd(datos["id_ruta"]):
        return None, None, {"id_ruta": "No existe una ruta logistica con ese id."}

    transportista = consultar_transportista_por_id_en_bd(datos["id_transportista"])
    if not transportista:
        return None, None, {"id_transportista": "No existe transportista con ese id."}
    if not transportista.activo:
        return None, None, {"id_transportista": "El transportista no esta activo."}

    tipo_salida = consultar_tipo_movimiento_inventario_por_nombre_en_bd("TRANSFERENCIA_SALIDA")
    if not tipo_salida:
        return None, None, {"tipo_movimiento": "No existe TRANSFERENCIA_SALIDA."}

    try:
        descontar_inventario_origen_por_envio(transferencia, tipo_salida.id_tipo_movimiento)

        envio = EnvioTransferencia(
            id_transferencia=transferencia.id_transferencia,
            id_ruta=datos["id_ruta"],
            id_transportista=datos["id_transportista"],
            fecha_envio=datetime.utcnow(),
            fecha_estimada_llegada=convertir_texto_a_fecha_hora(
                datos.get("fecha_estimada_llegada"),
            ),
            estado_envio="EN_TRANSITO",
        )
        db.session.add(envio)

        estado_enviada = obtener_estado_transferencia("ENVIADA")
        transferencia.id_estado_transferencia = estado_enviada.id_estado_transferencia
        db.session.add(transferencia)
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise

    return (
        convertir_transferencia_a_respuesta(transferencia),
        convertir_envio_transferencia_a_respuesta(envio),
        None,
    )


def confirmar_recepcion_transferencia_con_validaciones(id_transferencia, datos):
    """Confirma recepcion completa o parcial y actualiza inventario destino."""
    errores = validar_datos_para_confirmar_recepcion_transferencia(datos)
    if errores:
        return None, None, errores

    transferencia = consultar_transferencia_por_id_en_bd(id_transferencia)
    if not transferencia:
        return None, None, {"transferencia": "No existe una transferencia con ese id."}

    if obtener_nombre_estado(transferencia) != "ENVIADA":
        return None, None, {"estado": "Solo se pueden recibir transferencias ENVIADAS."}

    if not consultar_usuario_por_id_en_bd(datos["id_usuario_recibe"]):
        return None, None, {"id_usuario_recibe": "No existe usuario con ese id."}

    envio = consultar_envio_por_transferencia_en_bd(id_transferencia)
    if not envio:
        return None, None, {"envio": "La transferencia no tiene envio registrado."}

    tipo_entrada = consultar_tipo_movimiento_inventario_por_nombre_en_bd("TRANSFERENCIA_ENTRADA")
    if not tipo_entrada:
        return None, None, {"tipo_movimiento": "No existe TRANSFERENCIA_ENTRADA."}

    recepciones_por_detalle, errores_cantidades = preparar_cantidades_recibidas(
        transferencia,
        datos["detalles"],
    )
    if errores_cantidades:
        return None, None, errores_cantidades

    try:
        recepcion = RecepcionTransferencia(
            id_transferencia=transferencia.id_transferencia,
            id_usuario_recibe=datos["id_usuario_recibe"],
            fecha_recepcion=datetime.utcnow(),
            tipo_recepcion="COMPLETA",
            observacion=(datos.get("observacion") or "").strip() or None,
        )
        db.session.add(recepcion)
        db.session.flush()

        es_parcial = aplicar_recepcion_en_inventario_destino(
            transferencia,
            recepcion,
            recepciones_por_detalle,
            tipo_entrada.id_tipo_movimiento,
        )

        estado_final = obtener_estado_transferencia(
            "RECIBIDA_PARCIAL" if es_parcial else "RECIBIDA"
        )
        transferencia.id_estado_transferencia = estado_final.id_estado_transferencia
        recepcion.tipo_recepcion = "PARCIAL" if es_parcial else "COMPLETA"
        envio.fecha_real_llegada = recepcion.fecha_recepcion
        envio.estado_envio = "ENTREGADO_PARCIAL" if es_parcial else "ENTREGADO"

        db.session.add(transferencia)
        db.session.add(recepcion)
        db.session.add(envio)
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise

    return (
        convertir_transferencia_a_respuesta(transferencia),
        convertir_recepcion_transferencia_a_respuesta(recepcion),
        None,
    )


def validar_relaciones_de_solicitud(datos):
    """Valida sucursales, usuario, productos y unidades de la solicitud."""
    errores = {}

    if not consultar_sucursal_por_id_en_bd(datos["id_sucursal_origen"]):
        errores["id_sucursal_origen"] = "No existe sucursal origen con ese id."

    if not consultar_sucursal_por_id_en_bd(datos["id_sucursal_destino"]):
        errores["id_sucursal_destino"] = "No existe sucursal destino con ese id."

    if not consultar_usuario_por_id_en_bd(datos["id_usuario_solicita"]):
        errores["id_usuario_solicita"] = "No existe usuario con ese id."

    for posicion, detalle in enumerate(datos["detalles"], start=1):
        producto = consultar_producto_por_id_en_bd(detalle["id_producto"])
        producto_unidad = consultar_producto_unidad_por_id_en_bd(detalle["id_producto_unidad"])

        if not producto:
            errores[f"detalle_{posicion}_id_producto"] = "No existe producto con ese id."
        elif not producto.activo:
            errores[f"detalle_{posicion}_id_producto"] = "El producto no esta activo."

        if not producto_unidad:
            errores[f"detalle_{posicion}_id_producto_unidad"] = (
                "No existe una unidad asociada a producto con ese id."
            )
        elif producto_unidad.id_producto != detalle["id_producto"]:
            errores[f"detalle_{posicion}_id_producto_unidad"] = (
                "La unidad indicada no pertenece al producto."
            )

    return errores


def construir_detalles_de_solicitud(detalles_recibidos):
    """Construye detalles solicitados con cantidades aprobadas/recibidas en cero."""
    detalles = []
    for detalle_recibido in detalles_recibidos:
        detalles.append(DetalleTransferencia(
            id_producto=detalle_recibido["id_producto"],
            id_producto_unidad=detalle_recibido["id_producto_unidad"],
            cantidad_solicitada=convertir_valor_a_decimal(detalle_recibido["cantidad_solicitada"]),
            cantidad_aprobada=0,
            cantidad_recibida=0,
        ))

    return detalles


def aplicar_cantidades_aprobadas(transferencia, detalles_aprobados):
    """Ajusta cantidades a enviar y valida disponibilidad en sucursal origen."""
    errores = {}
    detalles_por_id = {
        detalle.id_detalle_transferencia: detalle for detalle in transferencia.detalles
    }

    for posicion, datos_detalle in enumerate(detalles_aprobados, start=1):
        detalle = detalles_por_id.get(datos_detalle["id_detalle_transferencia"])
        if not detalle:
            errores[f"detalle_{posicion}"] = "El detalle no pertenece a la transferencia."
            continue

        cantidad_aprobada = convertir_valor_a_decimal(datos_detalle["cantidad_aprobada"])
        if cantidad_aprobada > detalle.cantidad_solicitada:
            errores[f"detalle_{posicion}_cantidad_aprobada"] = (
                "No se puede aprobar mas de lo solicitado."
            )
            continue

        inventario = consultar_inventario_por_sucursal_y_producto_en_bd(
            transferencia.id_sucursal_origen,
            detalle.id_producto,
        )
        if not inventario or inventario.cantidad_actual < cantidad_aprobada:
            errores[f"detalle_{posicion}_stock"] = (
                "La sucursal origen no tiene stock suficiente para esa cantidad."
            )
            continue

        detalle.cantidad_aprobada = cantidad_aprobada
        db.session.add(detalle)

    if errores:
        return errores

    if not any(detalle.cantidad_aprobada > 0 for detalle in transferencia.detalles):
        return {"detalles": "Debe aprobar al menos una cantidad mayor a cero."}

    return None


def descontar_inventario_origen_por_envio(transferencia, id_tipo_salida):
    """Descuenta stock de origen y registra movimientos de salida por transferencia."""
    for detalle in transferencia.detalles:
        if detalle.cantidad_aprobada <= 0:
            continue

        inventario = consultar_inventario_por_sucursal_y_producto_en_bd(
            transferencia.id_sucursal_origen,
            detalle.id_producto,
        )
        if not inventario or inventario.cantidad_actual < detalle.cantidad_aprobada:
            raise ValueError("Stock insuficiente al registrar el envio de transferencia.")

        inventario.cantidad_actual -= detalle.cantidad_aprobada
        db.session.add(inventario)
        db.session.flush()

        db.session.add(MovimientoInventario(
            id_inventario=inventario.id_inventario,
            id_usuario=transferencia.id_usuario_solicita,
            id_tipo_movimiento=id_tipo_salida,
            motivo=f"Envio de transferencia {transferencia.id_transferencia}",
            cantidad=detalle.cantidad_aprobada,
            modulo_origen="TRANSFERENCIA",
            id_origen=transferencia.id_transferencia,
        ))


def preparar_cantidades_recibidas(transferencia, detalles_recibidos):
    """Valida cantidades recibidas contra cantidades aprobadas."""
    errores = {}
    cantidades = {}
    detalles_por_id = {
        detalle.id_detalle_transferencia: detalle for detalle in transferencia.detalles
    }

    for posicion, datos_detalle in enumerate(detalles_recibidos, start=1):
        detalle = detalles_por_id.get(datos_detalle["id_detalle_transferencia"])
        if not detalle:
            errores[f"detalle_{posicion}"] = "El detalle no pertenece a la transferencia."
            continue

        cantidad_recibida = convertir_cantidad_recepcion(datos_detalle["cantidad_recibida"])
        if cantidad_recibida > detalle.cantidad_aprobada:
            errores[f"detalle_{posicion}_cantidad_recibida"] = (
                "No se puede recibir mas de la cantidad aprobada."
            )
            continue

        faltante = detalle.cantidad_aprobada - cantidad_recibida
        tratamiento = (datos_detalle.get("tratamiento") or "").strip().upper()
        if faltante > 0 and not tratamiento:
            errores[f"detalle_{posicion}_tratamiento"] = (
                "Debe indicar tratamiento para el faltante."
            )

        cantidades[detalle.id_detalle_transferencia] = {
            "detalle": detalle,
            "cantidad_recibida": cantidad_recibida,
            "faltante": faltante,
            "tratamiento": tratamiento,
            "descripcion": (datos_detalle.get("descripcion") or "").strip() or None,
        }

    for detalle in transferencia.detalles:
        if detalle.cantidad_aprobada > 0 and detalle.id_detalle_transferencia not in cantidades:
            errores[f"detalle_{detalle.id_detalle_transferencia}"] = (
                "Debe indicar la cantidad recibida de cada producto aprobado."
            )

    return cantidades, errores


def aplicar_recepcion_en_inventario_destino(
    transferencia,
    recepcion,
    recepciones_por_detalle,
    id_tipo_entrada,
):
    """Suma stock destino, actualiza detalles y registra incidencias si faltan."""
    es_parcial = False

    for datos in recepciones_por_detalle.values():
        detalle = datos["detalle"]
        cantidad_recibida = datos["cantidad_recibida"]
        faltante = datos["faltante"]

        detalle.cantidad_recibida = cantidad_recibida
        db.session.add(detalle)

        if cantidad_recibida > 0:
            inventario = consultar_inventario_por_sucursal_y_producto_en_bd(
                transferencia.id_sucursal_destino,
                detalle.id_producto,
            )
            if not inventario:
                inventario = InventarioSucursal(
                    id_sucursal=transferencia.id_sucursal_destino,
                    id_producto=detalle.id_producto,
                    cantidad_actual=0,
                    costo_promedio=0,
                )

            inventario.cantidad_actual += cantidad_recibida
            db.session.add(inventario)
            db.session.flush()

            db.session.add(MovimientoInventario(
                id_inventario=inventario.id_inventario,
                id_usuario=recepcion.id_usuario_recibe,
                id_tipo_movimiento=id_tipo_entrada,
                motivo=f"Recepcion de transferencia {transferencia.id_transferencia}",
                cantidad=cantidad_recibida,
                modulo_origen="TRANSFERENCIA",
                id_origen=transferencia.id_transferencia,
            ))

        if faltante > 0:
            es_parcial = True
            db.session.add(IncidenciaTransferencia(
                id_recepcion=recepcion.id_recepcion,
                id_detalle_transferencia=detalle.id_detalle_transferencia,
                cantidad_faltante=faltante,
                tratamiento=datos["tratamiento"],
                descripcion=datos["descripcion"],
            ))

    return es_parcial


def obtener_estado_transferencia(nombre):
    """Consulta un estado normalizado por nombre."""
    return consultar_estado_transferencia_por_nombre_en_bd(nombre)


def obtener_nombre_estado(transferencia):
    """Devuelve el nombre del estado normalizado de la transferencia."""
    return transferencia.estado_transferencia.nombre if transferencia.estado_transferencia else None
