import { ApiResponseDto } from '../../../models/api-response.dto';

export interface DashboardSalesPeriodDto {
  readonly anio: number;
  readonly mes: number;
  readonly periodo: string;
  readonly cantidad_ventas: number;
  readonly total_ventas: number;
}

export interface SalesSummaryDto {
  readonly mes_actual: DashboardSalesPeriodDto;
  readonly promedio_periodos_anteriores: number;
  readonly variacion_frente_promedio: number;
  readonly periodos: DashboardSalesPeriodDto[];
}

export interface ProductDemandMetricDto {
  readonly id_producto: number;
  readonly producto: string | null;
  readonly cantidad_vendida: number;
  readonly stock_actual: number;
  readonly indice_rotacion: number;
}

export interface DemandSummaryDto {
  readonly productos_alta_demanda: ProductDemandMetricDto[];
  readonly productos_baja_demanda: ProductDemandMetricDto[];
  readonly rotacion_inventario: ProductDemandMetricDto[];
}

export type EstadoReabastecimientoDto = 'AGOTADO' | 'BAJO_MINIMO' | 'PROXIMO_A_AGOTARSE';

export interface InventoryAlertDto {
  readonly id_sucursal: number;
  readonly id_producto: number;
  readonly producto: string;
  readonly codigo_producto: string;
  readonly cantidad_actual: number;
  readonly stock_minimo: number;
  readonly cantidad_faltante: number;
  readonly estado_reabastecimiento: EstadoReabastecimientoDto;
}

export interface TransferImpactDto {
  readonly id_producto: number;
  readonly producto: string | null;
  readonly cantidad_solicitada: number;
  readonly cantidad_aprobada: number;
  readonly cantidad_recibida: number;
}

export interface ActiveTransferDto {
  readonly id_transferencia: number;
  readonly estado: string | null;
  readonly id_sucursal_origen: number;
  readonly id_sucursal_destino: number;
  readonly fecha_solicitud: string | null;
  readonly cantidad_solicitada: number;
  readonly cantidad_aprobada: number;
  readonly cantidad_recibida: number;
  readonly cantidad_pendiente: number;
  readonly impacto_inventario: TransferImpactDto[];
}

export interface BranchPerformanceDto {
  readonly id_sucursal: number;
  readonly sucursal: string;
  readonly cantidad_ventas: number;
  readonly total_ventas: number;
  readonly productos_bajo_stock: number;
  readonly transferencias_activas: number;
}

export type DashboardResponseDto<T> = ApiResponseDto<T>;
