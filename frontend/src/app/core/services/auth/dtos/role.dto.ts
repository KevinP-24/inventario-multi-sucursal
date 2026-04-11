import { UserRoleDto } from './user-role.dto';

export interface RoleDto {
  readonly id_rol: number;
  readonly nombre: string;
  readonly codigo: UserRoleDto | null;
  readonly descripcion?: string | null;
  readonly activo?: boolean;
}

export interface SaveRoleDto {
  readonly nombre: string;
  readonly descripcion?: string | null;
}
