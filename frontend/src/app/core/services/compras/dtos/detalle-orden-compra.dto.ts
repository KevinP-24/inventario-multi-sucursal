export interface DetalleOrdenCompraDto {
  readonly id_detalle_oc: number;
  readonly id_orden_compra: number;
  readonly id_producto: number;
  readonly id_producto_unidad: number;
  readonly cantidad: number;
  readonly precio_unitario: number;
  readonly descuento: number;
  readonly subtotal: number;
}

export interface CrearDetalleOrdenCompraDto {
  readonly id_producto: number;
  readonly id_producto_unidad: number;
  readonly cantidad: number;
  readonly precio_unitario: number;
  readonly descuento?: number;
}
