export interface ReporteFiltrosDto {
  readonly fecha_desde?: string;
  readonly fecha_hasta?: string;
  readonly id_sucursal?: number;
  readonly [key: string]: string | number | undefined;
}
