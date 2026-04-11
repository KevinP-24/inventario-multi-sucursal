export interface DetalleCompra {
  readonly id_detalle_oc: number;
  readonly id_orden_compra: number;
  readonly id_producto: number;
  readonly id_producto_unidad: number;
  readonly cantidad: number;
  readonly precio_unitario: number;
  readonly descuento: number;
  readonly subtotal: number;
}

export type EstadoCompra = 'CREADA' | 'RECIBIDA' | 'ANULADA';

export interface Compra {
  readonly id_orden_compra: number;
  readonly id_proveedor: number;
  readonly id_sucursal: number;
  readonly id_usuario: number;
  readonly fecha: string | null;
  readonly estado: EstadoCompra | string;
  readonly plazo_pago: string | null;
  readonly subtotal: number;
  readonly descuento_total: number;
  readonly total: number;
  readonly fecha_recepcion: string | null;
  readonly id_usuario_recepcion: number | null;
  readonly detalles?: DetalleCompra[];
}

export interface CrearCompraPayload {
  readonly id_proveedor: number;
  readonly id_sucursal: number;
  readonly id_usuario: number;
  readonly fecha?: string;
  readonly plazo_pago?: string | null;
  readonly detalles: Omit<DetalleCompra, 'id_detalle_oc' | 'id_orden_compra' | 'subtotal'>[];
}

export interface HistorialComprasFiltros {
  readonly id_proveedor?: number;
  readonly id_producto?: number;
  readonly id_sucursal?: number;
  readonly estado?: EstadoCompra;
  readonly fecha_desde?: string;
  readonly fecha_hasta?: string;
}

export interface RecibirCompraPayload {
  readonly id_usuario_recepcion: number;
}

export interface CompraRecepcionResultado {
  readonly orden_compra: Compra;
  readonly movimientos_inventario: Record<string, unknown>[];
}
