import { AuthUserDto } from './auth-user.dto';

export type UserDto = AuthUserDto;

export interface SaveUserDto {
  readonly id_rol: number;
  readonly id_sucursal?: number | null;
  readonly nombre: string;
  readonly correo: string;
  readonly password?: string;
  readonly activo?: boolean;
}
