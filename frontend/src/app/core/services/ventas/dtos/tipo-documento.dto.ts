export interface TipoDocumentoDto {
  readonly id_tipo_documento: number;
  readonly codigo: string;
  readonly nombre: string;
  readonly descripcion: string | null;
  readonly activo: boolean;
}
