export interface IncidenciaTransferenciaDto {
  readonly id_incidencia: number;
  readonly id_recepcion: number;
  readonly id_detalle_transferencia: number;
  readonly cantidad_faltante: number;
  readonly tratamiento: string;
  readonly descripcion: string | null;
}
