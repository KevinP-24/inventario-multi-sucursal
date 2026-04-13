import { IncidenciaTransferenciaDto } from './incidencia-transferencia.dto';

export interface RecepcionTransferenciaDto {
  readonly id_recepcion: number;
  readonly id_transferencia: number;
  readonly id_usuario_recibe: number;
  readonly fecha_recepcion: string | null;
  readonly tipo_recepcion: string;
  readonly observacion: string | null;
  readonly incidencias: IncidenciaTransferenciaDto[];
}

export interface ConfirmarRecepcionTransferenciaDto {
  readonly id_usuario_recibe: number;
  readonly tipo_recepcion?: string;
  readonly observacion?: string | null;
  readonly detalles: {
    readonly id_detalle_transferencia: number;
    readonly cantidad_recibida: number;
    readonly tratamiento?: string;
    readonly descripcion?: string | null;
  }[];
}
