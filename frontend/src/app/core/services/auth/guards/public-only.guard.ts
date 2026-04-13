import { inject } from '@angular/core';
import { CanActivateFn, Router } from '@angular/router';

import { AuthSessionService } from '../auth-session.service';
import { getDefaultRouteByRole } from '../utils/auth-redirect.util';

export const publicOnlyGuard: CanActivateFn = () => {
  const authSession = inject(AuthSessionService);
  const router = inject(Router);

  if (!authSession.isAuthenticated()) {
    return true;
  }

  return router.createUrlTree([
    getDefaultRouteByRole(authSession.currentUser()?.rol?.codigo ?? null)
  ]);
};