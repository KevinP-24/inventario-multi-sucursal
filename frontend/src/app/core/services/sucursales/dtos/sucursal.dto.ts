export type EstadoSucursalDto = 'activa' | 'inactiva';

export interface SucursalDto {
  readonly id_sucursal: number;
  readonly nombre: string;
  readonly direccion: string;
  readonly ciudad: string;
  readonly telefono: string | null;
  readonly estado: string;
}

export interface GuardarSucursalDto {
  readonly nombre: string;
  readonly direccion: string;
  readonly ciudad: string;
  readonly telefono?: string | null;
  readonly estado?: EstadoSucursalDto;
}
