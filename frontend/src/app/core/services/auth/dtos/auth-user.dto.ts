import { RoleDto } from './role.dto';

export interface AuthBranchDto {
  readonly id_sucursal: number;
  readonly nombre: string;
  readonly direccion?: string | null;
  readonly ciudad?: string | null;
  readonly telefono?: string | null;
  readonly estado?: string | null;
}

export interface AuthUserDto {
  readonly id_usuario: number;
  readonly id_rol: number;
  readonly id_sucursal: number | null;
  readonly nombre: string;
  readonly correo: string;
  readonly activo: boolean;
  readonly fecha_creacion?: string | null;
  readonly rol: RoleDto | null;
  readonly sucursal: AuthBranchDto | null;
}
