export interface TransportistaDto {
  readonly id_transportista: number;
  readonly identificacion: string;
  readonly nombre: string;
  readonly telefono: string | null;
  readonly activo: boolean;
}

export interface GuardarTransportistaDto {
  readonly identificacion: string;
  readonly nombre: string;
  readonly telefono?: string | null;
  readonly activo?: boolean;
}
