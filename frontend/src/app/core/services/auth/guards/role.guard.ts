import { inject } from '@angular/core';
import { CanActivateFn, Router } from '@angular/router';

import { AuthSessionService } from '../auth-session.service';
import { ROLE_ROUTES } from '../config/role-routes.config';
import { UserRoleDto } from '../dtos/user-role.dto';
import { getDefaultRouteByRole } from '../utils/auth-redirect.util';

export const roleGuard =
    (allowedRoles: UserRoleDto[]): CanActivateFn =>
    (_, state) => {
        const authSession = inject(AuthSessionService);
        const router = inject(Router);

        if (!authSession.isAuthenticated()) {
        return router.createUrlTree(['/login']);
        }

        const currentUser = authSession.currentUser();
        const role = currentUser?.rol?.codigo ?? undefined;

        if (!role || !allowedRoles.includes(role)) {
        return router.createUrlTree([getDefaultRouteByRole(role)]);
        }

        const allowedRoutes = ROLE_ROUTES[role] ?? [];
        const targetUrl = state.url;

        const hasAccess = allowedRoutes.some((route) => targetUrl.startsWith(route));

        return hasAccess
        ? true
        : router.createUrlTree([getDefaultRouteByRole(role)]);
};
