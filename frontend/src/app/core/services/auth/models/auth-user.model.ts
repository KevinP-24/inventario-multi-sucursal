import { UserRole } from './user-role.model';

export interface AuthRole {
  readonly id_rol: number;
  readonly nombre: string;
  readonly codigo: UserRole | null;
  readonly descripcion?: string | null;
  readonly activo?: boolean;
}

export interface AuthBranch {
  readonly id_sucursal: number;
  readonly nombre: string;
  readonly direccion?: string | null;
  readonly ciudad?: string | null;
  readonly telefono?: string | null;
  readonly estado?: string | null;
}

export interface AuthUser {
  readonly id_usuario: number;
  readonly id_rol: number;
  readonly id_sucursal: number | null;
  readonly nombre: string;
  readonly correo: string;
  readonly activo: boolean;
  readonly fecha_creacion?: string | null;
  readonly rol: AuthRole | null;
  readonly sucursal: AuthBranch | null;
}