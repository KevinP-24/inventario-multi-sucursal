import { AuthUser } from './auth-user.model';

export interface LoginResponse {
  readonly message: string;
  readonly access_token: string;
  readonly token_type: 'Bearer';
  readonly usuario: AuthUser;
}

export interface MeResponse {
  readonly data: AuthUser;
}
