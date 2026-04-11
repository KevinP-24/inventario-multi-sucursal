export interface DetalleVentaDto {
  readonly id_detalle_venta: number;
  readonly id_venta: number;
  readonly id_producto: number;
  readonly id_producto_unidad: number;
  readonly cantidad: number;
  readonly precio_unitario: number;
  readonly descuento: number;
  readonly subtotal: number;
}

export interface CrearDetalleVentaDto {
  readonly id_producto: number;
  readonly id_producto_unidad: number;
  readonly cantidad: number;
  readonly descuento?: number;
}
