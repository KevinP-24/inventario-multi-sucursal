export interface RutaLogisticaDto {
  readonly id_ruta: number;
  readonly nombre_ruta: string;
  readonly id_prioridad_ruta: number;
  readonly prioridad: string | null;
  readonly costo_estimado: number;
  readonly tiempo_estimado: string | null;
}

export interface GuardarRutaLogisticaDto {
  readonly nombre_ruta: string;
  readonly id_prioridad_ruta?: number;
  readonly prioridad?: string;
  readonly costo_estimado?: number;
  readonly tiempo_estimado?: string | null;
}

export type CriterioClasificacionRutaLogisticaDto = 'prioridad' | 'costo' | 'tiempo';
