import { EnvioTransferenciaDto } from '../../logistica/dtos/envio-transferencia.dto';
import { DetalleTransferenciaDto, CrearDetalleTransferenciaDto, RevisionTransferenciaDetalleDto } from './detalle-transferencia.dto';
import { RecepcionTransferenciaDto } from './recepcion-transferencia.dto';

export type PrioridadTransferenciaDto = 'BAJA' | 'NORMAL' | 'ALTA' | 'URGENTE';
export type AccionRevisionTransferenciaDto = 'APROBAR' | 'RECHAZAR';

export interface TransferenciaDto {
  readonly id_transferencia: number;
  readonly id_sucursal_origen: number;
  readonly id_sucursal_destino: number;
  readonly id_usuario_solicita: number;
  readonly id_estado_transferencia: number;
  readonly fecha_solicitud: string | null;
  readonly prioridad: PrioridadTransferenciaDto | string;
  readonly estado: string | null;
  readonly observacion: string | null;
  readonly detalles?: DetalleTransferenciaDto[];
  readonly envio?: EnvioTransferenciaDto;
}

export interface CrearTransferenciaDto {
  readonly id_sucursal_origen: number;
  readonly id_sucursal_destino: number;
  readonly id_usuario_solicita: number;
  readonly prioridad?: PrioridadTransferenciaDto;
  readonly observacion?: string | null;
  readonly detalles: CrearDetalleTransferenciaDto[];
}

export interface RevisarTransferenciaDto {
  readonly accion: AccionRevisionTransferenciaDto;
  readonly detalles?: RevisionTransferenciaDetalleDto[];
  readonly observacion?: string | null;
}

export interface RegistrarEnvioTransferenciaDto {
  readonly id_ruta: number;
  readonly id_transportista: number;
  readonly fecha_estimada_llegada?: string | null;
}

export interface RegistrarEnvioTransferenciaResultadoDto {
  readonly transferencia: TransferenciaDto;
  readonly envio: EnvioTransferenciaDto;
}

export interface ConfirmarRecepcionTransferenciaResultadoDto {
  readonly transferencia: TransferenciaDto;
  readonly recepcion: RecepcionTransferenciaDto;
}
