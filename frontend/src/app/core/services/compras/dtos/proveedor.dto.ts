export interface TipoDocumentoProveedorDto {
  readonly id_tipo_documento: number;
  readonly nombre?: string;
  readonly codigo?: string;
  readonly descripcion?: string | null;
  readonly activo?: boolean;
}

export interface ProveedorDto {
  readonly id_proveedor: number;
  readonly id_tipo_documento: number;
  readonly tipo_documento: TipoDocumentoProveedorDto | null;
  readonly numero_documento: string;
  readonly nombre: string;
  readonly correo: string | null;
  readonly telefono: string | null;
  readonly direccion: string | null;
  readonly activo: boolean;
}

export interface GuardarProveedorDto {
  readonly id_tipo_documento: number;
  readonly numero_documento: string;
  readonly nombre: string;
  readonly correo?: string | null;
  readonly telefono?: string | null;
  readonly direccion?: string | null;
  readonly activo?: boolean;
}
