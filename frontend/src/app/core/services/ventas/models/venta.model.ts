export interface DetalleVenta {
  readonly id_detalle_venta: number;
  readonly id_venta: number;
  readonly id_producto: number;
  readonly id_producto_unidad: number;
  readonly cantidad: number;
  readonly precio_unitario: number;
  readonly descuento: number;
  readonly subtotal: number;
}

export type EstadoVenta = 'CONFIRMADA' | 'ANULADA';

export interface ClienteVenta {
  readonly [key: string]: unknown;
}

export interface Venta {
  readonly id_venta: number;
  readonly id_sucursal: number;
  readonly id_usuario: number;
  readonly id_cliente: number | null;
  readonly id_lista_precio: number;
  readonly fecha: string | null;
  readonly descuento_total: number;
  readonly total: number;
  readonly comprobante: string;
  readonly estado: EstadoVenta | string;
  readonly cliente: ClienteVenta | null;
  readonly detalles?: DetalleVenta[];
}

export interface CrearVentaPayload {
  readonly id_sucursal: number;
  readonly id_usuario: number;
  readonly id_cliente?: number | null;
  readonly id_lista_precio: number;
  readonly detalles: Omit<DetalleVenta, 'id_detalle_venta' | 'id_venta' | 'precio_unitario' | 'subtotal'>[];
}
