export interface UnidadMedidaDto {
  readonly id_unidad: number;
  readonly nombre: string;
  readonly simbolo: string;
  readonly activo: boolean;
}

export interface GuardarUnidadMedidaDto {
  readonly nombre: string;
  readonly simbolo: string;
}
