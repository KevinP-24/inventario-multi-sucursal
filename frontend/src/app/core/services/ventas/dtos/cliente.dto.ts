import { TipoDocumentoDto } from './tipo-documento.dto';

export interface ClienteDto {
  readonly id_cliente: number;
  readonly id_tipo_documento: number;
  readonly tipo_documento: TipoDocumentoDto | null;
  readonly numero_documento: string;
  readonly nombre: string;
  readonly correo: string | null;
  readonly telefono: string | null;
  readonly activo: boolean;
  readonly fecha_creacion: string | null;
}

export interface GuardarClienteDto {
  readonly id_tipo_documento: number;
  readonly numero_documento: string;
  readonly nombre: string;
  readonly correo?: string | null;
  readonly telefono?: string | null;
}
