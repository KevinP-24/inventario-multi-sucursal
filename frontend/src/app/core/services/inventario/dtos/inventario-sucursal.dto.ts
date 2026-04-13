export interface InventarioSucursalDto {
  readonly id_inventario: number;
  readonly id_sucursal: number;
  readonly id_producto: number;
  readonly cantidad_actual: number;
  readonly costo_promedio: number;
}

export interface StockAlertDto {
  readonly id_inventario: number;
  readonly id_sucursal: number;
  readonly id_producto: number;
  readonly producto: string | null;
  readonly codigo_producto: string | null;
  readonly cantidad_actual: number;
  readonly stock_minimo: number;
  readonly cantidad_faltante: number;
}

export interface CrearInventarioSucursalDto {
  readonly id_sucursal: number;
  readonly id_producto: number;
  readonly cantidad_actual?: number;
  readonly costo_promedio?: number;
}

export interface ActualizarInventarioSucursalDto {
  readonly cantidad_actual?: number;
  readonly costo_promedio?: number;
}

export type TipoAjusteInventarioDto = 'ENTRADA' | 'SALIDA' | 'AJUSTE';

export interface AjustarInventarioDto {
  readonly id_usuario: number;
  readonly tipo_ajuste: TipoAjusteInventarioDto;
  readonly cantidad?: number;
  readonly cantidad_actual_nueva?: number;
  readonly motivo?: string | null;
}

export interface MovimientoOperativoInventarioDto {
  readonly id_usuario: number;
  readonly cantidad: number;
  readonly id_origen?: number | null;
  readonly motivo?: string | null;
}

export interface InventarioMovimientoResultadoDto {
  readonly inventario: InventarioSucursalDto;
  readonly movimiento: Record<string, unknown>;
}
