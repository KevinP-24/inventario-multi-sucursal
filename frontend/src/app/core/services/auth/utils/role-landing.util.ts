import { getDefaultRouteByRole } from './auth-redirect.util';
import { AuthUserDto } from '../dtos/auth-user.dto';

export function resolveLandingRoute(user: AuthUserDto | null): string {
  return getDefaultRouteByRole(user?.rol?.codigo);
}
