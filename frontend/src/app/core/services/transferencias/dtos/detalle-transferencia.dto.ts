export interface DetalleTransferenciaDto {
  readonly id_detalle_transferencia: number;
  readonly id_transferencia: number;
  readonly id_producto: number;
  readonly id_producto_unidad: number;
  readonly cantidad_solicitada: number;
  readonly cantidad_aprobada: number;
  readonly cantidad_recibida: number;
}

export interface CrearDetalleTransferenciaDto {
  readonly id_producto: number;
  readonly id_producto_unidad: number;
  readonly cantidad_solicitada: number;
}

export interface RevisionTransferenciaDetalleDto {
  readonly id_detalle_transferencia: number;
  readonly cantidad_aprobada: number;
}
