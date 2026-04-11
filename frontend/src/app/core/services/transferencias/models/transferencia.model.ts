export interface DetalleTransferencia {
  readonly id_detalle_transferencia: number;
  readonly id_transferencia: number;
  readonly id_producto: number;
  readonly id_producto_unidad: number;
  readonly cantidad_solicitada: number;
  readonly cantidad_aprobada: number;
  readonly cantidad_recibida: number;
}

export type PrioridadTransferencia = 'BAJA' | 'NORMAL' | 'ALTA' | 'URGENTE';
export type AccionRevisionTransferencia = 'APROBAR' | 'RECHAZAR';

export interface EnvioTransferencia {
  readonly [key: string]: unknown;
}

export interface IncidenciaTransferencia {
  readonly [key: string]: unknown;
}

export interface RecepcionTransferencia {
  readonly id_recepcion: number;
  readonly id_transferencia: number;
  readonly id_usuario_recibe: number;
  readonly fecha_recepcion: string | null;
  readonly tipo_recepcion: string;
  readonly observacion: string | null;
  readonly incidencias: IncidenciaTransferencia[];
}

export interface Transferencia {
  readonly id_transferencia: number;
  readonly id_sucursal_origen: number;
  readonly id_sucursal_destino: number;
  readonly id_usuario_solicita: number;
  readonly id_estado_transferencia: number;
  readonly fecha_solicitud: string | null;
  readonly prioridad: PrioridadTransferencia | string;
  readonly estado: string | null;
  readonly observacion: string | null;
  readonly detalles?: DetalleTransferencia[];
  readonly envio?: EnvioTransferencia;
}

export interface CrearTransferenciaPayload {
  readonly id_sucursal_origen: number;
  readonly id_sucursal_destino: number;
  readonly id_usuario_solicita: number;
  readonly prioridad?: PrioridadTransferencia;
  readonly observacion?: string | null;
  readonly detalles: Omit<
    DetalleTransferencia,
    'id_detalle_transferencia' | 'id_transferencia' | 'cantidad_aprobada' | 'cantidad_recibida'
  >[];
}

export interface RevisionTransferenciaDetallePayload {
  readonly id_detalle_transferencia: number;
  readonly cantidad_aprobada: number;
}

export interface RevisarTransferenciaPayload {
  readonly accion: AccionRevisionTransferencia;
  readonly detalles?: RevisionTransferenciaDetallePayload[];
}

export interface RegistrarEnvioTransferenciaPayload {
  readonly [key: string]: unknown;
}

export interface RegistrarEnvioTransferenciaResultado {
  readonly transferencia: Transferencia;
  readonly envio: EnvioTransferencia;
}

export interface ConfirmarRecepcionTransferenciaPayload {
  readonly [key: string]: unknown;
}

export interface ConfirmarRecepcionTransferenciaResultado {
  readonly transferencia: Transferencia;
  readonly recepcion: RecepcionTransferencia;
}
