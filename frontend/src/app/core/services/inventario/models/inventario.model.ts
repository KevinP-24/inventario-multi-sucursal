export interface Inventario {
  readonly id_inventario: number;
  readonly id_sucursal: number;
  readonly id_producto: number;
  readonly cantidad_actual: number;
  readonly costo_promedio: number;
}

export interface InventarioAlertaStock {
  readonly id_inventario: number;
  readonly id_sucursal: number;
  readonly id_producto: number;
  readonly producto: string | null;
  readonly codigo_producto: string | null;
  readonly cantidad_actual: number;
  readonly stock_minimo: number;
  readonly cantidad_faltante: number;
}

export interface CrearInventarioPayload {
  readonly id_sucursal: number;
  readonly id_producto: number;
  readonly cantidad_actual?: number;
  readonly costo_promedio?: number;
}

export interface ActualizarInventarioPayload {
  readonly cantidad_actual?: number;
  readonly costo_promedio?: number;
}

export type TipoAjusteInventario = 'ENTRADA' | 'SALIDA' | 'AJUSTE';

export interface AjustarInventarioPayload {
  readonly id_usuario: number;
  readonly tipo_ajuste: TipoAjusteInventario;
  readonly cantidad?: number;
  readonly cantidad_actual_nueva?: number;
}

export interface MovimientoOperativoInventarioPayload {
  readonly id_usuario: number;
  readonly cantidad: number;
  readonly id_origen?: number | null;
}

export interface InventarioMovimientoResultado {
  readonly inventario: Inventario;
  readonly movimiento: Record<string, unknown>;
}
