import { ApiResponseDto } from '../../../models/api-response.dto';
import { AuthUserDto } from './auth-user.dto';
import { RoleDto } from './role.dto';

export interface LoginResponseDto {
  readonly message: string;
  readonly access_token: string;
  readonly token_type: 'Bearer';
  readonly usuario: AuthUserDto;
}

export type MeResponseDto = ApiResponseDto<AuthUserDto>;
export type RolesResponseDto = ApiResponseDto<RoleDto[]>;
export type RoleResponseDto = ApiResponseDto<RoleDto>;
export type UsersResponseDto = ApiResponseDto<AuthUserDto[]>;
export type UserResponseDto = ApiResponseDto<AuthUserDto>;
