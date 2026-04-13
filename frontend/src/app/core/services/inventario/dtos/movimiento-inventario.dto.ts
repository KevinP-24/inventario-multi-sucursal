export interface MovimientoInventarioDto {
  readonly id_movimiento: number;
  readonly id_inventario: number;
  readonly id_usuario: number;
  readonly id_tipo_movimiento: number;
  readonly tipo_movimiento: string | null;
  readonly motivo: string | null;
  readonly cantidad: number;
  readonly fecha_hora: string | null;
  readonly modulo_origen: string | null;
  readonly id_origen: number | null;
}

export interface FiltrosMovimientoInventarioDto {
  readonly id_sucursal?: number;
  readonly id_producto?: number;
  readonly id_tipo_movimiento?: number;
  readonly modulo_origen?: string;
  readonly id_origen?: number;
  readonly fecha_desde?: string;
  readonly fecha_hasta?: string;
}

export interface RegistrarMovimientoInventarioDto {
  readonly id_inventario: number;
  readonly id_usuario: number;
  readonly id_tipo_movimiento: number;
  readonly motivo?: string | null;
  readonly cantidad: number;
  readonly modulo_origen?: string | null;
  readonly id_origen?: number | null;
}
