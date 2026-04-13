import { DetalleOrdenCompraDto, CrearDetalleOrdenCompraDto } from './detalle-orden-compra.dto';

export type EstadoOrdenCompraDto = 'CREADA' | 'RECIBIDA' | 'ANULADA';

export interface OrdenCompraDto {
  readonly id_orden_compra: number;
  readonly id_proveedor: number;
  readonly id_sucursal: number;
  readonly id_usuario: number;
  readonly fecha: string | null;
  readonly estado: EstadoOrdenCompraDto | string;
  readonly plazo_pago: string | null;
  readonly subtotal: number;
  readonly descuento_total: number;
  readonly total: number;
  readonly fecha_recepcion: string | null;
  readonly id_usuario_recepcion: number | null;
  readonly detalles?: DetalleOrdenCompraDto[];
}

export interface CrearOrdenCompraDto {
  readonly id_proveedor: number;
  readonly id_sucursal: number;
  readonly id_usuario: number;
  readonly fecha?: string;
  readonly plazo_pago?: string | null;
  readonly detalles: CrearDetalleOrdenCompraDto[];
}

export interface HistorialComprasFiltrosDto {
  readonly id_proveedor?: number;
  readonly id_producto?: number;
  readonly id_sucursal?: number;
  readonly estado?: EstadoOrdenCompraDto;
  readonly fecha_desde?: string;
  readonly fecha_hasta?: string;
}

export interface RecibirOrdenCompraDto {
  readonly id_usuario_recepcion: number;
}

export interface OrdenCompraRecepcionResultadoDto {
  readonly orden_compra: OrdenCompraDto;
  readonly movimientos_inventario: Record<string, unknown>[];
}
