import { AuthUser } from './auth-user.model';

export interface AuthSession {
  readonly accessToken: string;
  readonly tokenType: 'Bearer';
  readonly user: AuthUser;
}
