import { HttpErrorResponse, HttpInterceptorFn } from '@angular/common/http';
import { inject } from '@angular/core';
import { Router } from '@angular/router';
import { catchError, throwError } from 'rxjs';

import { environment } from '../../../../../environments/environment';
import { AuthSessionService } from '../auth-session.service';

export const jwtInterceptor: HttpInterceptorFn = (req, next) => {
  const authSession = inject(AuthSessionService);
  const router = inject(Router);
  const token = authSession.accessToken();

  const shouldAttachToken = token !== null && req.url.startsWith(environment.apiBaseUrl);
  const authRequest = shouldAttachToken
    ? req.clone({
        setHeaders: {
          Authorization: `Bearer ${token}`
        }
      })
    : req;

  return next(authRequest).pipe(
    catchError((error: HttpErrorResponse) => {
      const isProtectedApiCall = req.url.startsWith(environment.apiBaseUrl);
      const isLoginRequest = req.url.endsWith('/auth/login');

      if (error.status === 401 && isProtectedApiCall && !isLoginRequest) {
        authSession.logout();
        void router.navigate(['/login']);
      }

      return throwError(() => error);
    })
  );
};
