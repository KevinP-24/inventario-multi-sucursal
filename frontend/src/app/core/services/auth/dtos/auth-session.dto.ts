import { AuthUserDto } from './auth-user.dto';

export interface AuthSessionDto {
  readonly accessToken: string;
  readonly tokenType: 'Bearer';
  readonly user: AuthUserDto;
}
