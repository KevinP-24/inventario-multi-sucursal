export interface ParametroSistemaDto {
  readonly id_parametro: number;
  readonly clave: string;
  readonly valor: string;
  readonly descripcion: string | null;
  readonly activo: boolean;
}

export interface GuardarParametroSistemaDto {
  readonly clave: string;
  readonly valor: string;
  readonly descripcion?: string | null;
  readonly activo?: boolean;
}
