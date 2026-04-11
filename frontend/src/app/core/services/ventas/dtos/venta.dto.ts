import { ClienteDto } from './cliente.dto';
import { CrearDetalleVentaDto, DetalleVentaDto } from './detalle-venta.dto';

export type EstadoVentaDto = 'CONFIRMADA' | 'ANULADA';

export interface VentaDto {
  readonly id_venta: number;
  readonly id_sucursal: number;
  readonly id_usuario: number;
  readonly id_cliente: number | null;
  readonly id_lista_precio: number;
  readonly fecha: string | null;
  readonly descuento_total: number;
  readonly total: number;
  readonly comprobante: string;
  readonly estado: EstadoVentaDto | string;
  readonly cliente: ClienteDto | null;
  readonly detalles?: DetalleVentaDto[];
}

export interface CrearVentaDto {
  readonly id_sucursal: number;
  readonly id_usuario: number;
  readonly id_cliente?: number | null;
  readonly id_lista_precio: number;
  readonly detalles: CrearDetalleVentaDto[];
}
