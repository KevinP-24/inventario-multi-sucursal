import { computed, Injectable, signal } from '@angular/core';
import { catchError, map, Observable, of, tap } from 'rxjs';

import { AuthApiService } from './auth-api.service';
import { AuthCredentials } from './models/auth-credentials.model';
import { AuthSession } from './models/auth-session.model';
import { AuthUser } from './models/auth-user.model';

const AUTH_STORAGE_KEY = 'multi-sucursal.auth.session';

@Injectable({
  providedIn: 'root'
})
export class AuthSessionService {
  private readonly sessionState = signal<AuthSession | null>(this.readStoredSession());

  readonly session = computed(() => this.sessionState());
  readonly currentUser = computed(() => this.sessionState()?.user ?? null);
  readonly accessToken = computed(() => this.sessionState()?.accessToken ?? null);
  readonly isAuthenticated = computed(() => this.sessionState() !== null);

  constructor(private readonly authApi: AuthApiService) {}

  login(credentials: AuthCredentials): Observable<AuthUser> {
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

  restoreSession(): Observable<AuthUser | null> {
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

  private saveSession(session: AuthSession) {
    this.sessionState.set(session);
    localStorage.setItem(AUTH_STORAGE_KEY, JSON.stringify(session));
  }

  private clearSession() {
    this.sessionState.set(null);
    localStorage.removeItem(AUTH_STORAGE_KEY);
  }

  private readStoredSession(): AuthSession | null {
    const rawSession = localStorage.getItem(AUTH_STORAGE_KEY);
    if (!rawSession) {
      return null;
    }

    try {
      return JSON.parse(rawSession) as AuthSession;
    } catch {
      localStorage.removeItem(AUTH_STORAGE_KEY);
      return null;
    }
  }
}
