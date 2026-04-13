import { computed, Injectable, signal } from '@angular/core';
import { catchError, map, Observable, of, tap } from 'rxjs';

import { AuthApiService } from './auth-api.service';
import { AuthCredentialsDto } from './dtos/auth-credentials.dto';
import { AuthSessionDto } from './dtos/auth-session.dto';
import { AuthUserDto } from './dtos/auth-user.dto';

const AUTH_STORAGE_KEY = 'multi-sucursal.auth.session';

@Injectable({
  providedIn: 'root'
})
export class AuthSessionService {
  private readonly sessionState = signal<AuthSessionDto | null>(this.readStoredSession());

  readonly session = computed(() => this.sessionState());
  readonly currentUser = computed(() => this.sessionState()?.user ?? null);
  readonly accessToken = computed(() => this.sessionState()?.accessToken ?? null);
  readonly isAuthenticated = computed(() => this.sessionState() !== null);

  constructor(private readonly authApi: AuthApiService) {}

  login(credentials: AuthCredentialsDto): Observable<AuthUserDto> {
    return this.authApi.login(credentials).pipe(
      tap((response) =>
        this.saveSession({
          accessToken: response.access_token,
          tokenType: response.token_type,
          user: response.usuario
        })
      ),
      map((response) => response.usuario)
    );
  }

  restoreSession(): Observable<AuthUserDto | null> {
    if (!this.accessToken()) {
      return of(null);
    }

    return this.authApi.me().pipe(
      tap((response) => {
        const session = this.sessionState();
        if (!session) {
          return;
        }

        this.saveSession({
          ...session,
          user: response.data
        });
      }),
      map((response) => response.data),
      catchError(() => {
        this.clearSession();
        return of(null);
      })
    );
  }

  logout() {
    this.clearSession();
  }

  private saveSession(session: AuthSessionDto) {
    this.sessionState.set(session);
    localStorage.setItem(AUTH_STORAGE_KEY, JSON.stringify(session));
  }

  private clearSession() {
    this.sessionState.set(null);
    localStorage.removeItem(AUTH_STORAGE_KEY);
  }

  private readStoredSession(): AuthSessionDto | null {
    const rawSession = localStorage.getItem(AUTH_STORAGE_KEY);
    if (!rawSession) {
      return null;
    }

    try {
      return JSON.parse(rawSession) as AuthSessionDto;
    } catch {
      localStorage.removeItem(AUTH_STORAGE_KEY);
      return null;
    }
  }
}
