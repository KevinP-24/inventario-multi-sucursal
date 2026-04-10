import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';

import { environment } from '../../../../environments/environment';
import { AuthCredentials } from './models/auth-credentials.model';
import { LoginResponse, MeResponse } from './models/auth-response.model';

@Injectable({
  providedIn: 'root'
})
export class AuthApiService {
  private readonly http = inject(HttpClient);
  private readonly authUrl = `${environment.apiBaseUrl}/auth`;

  login(credentials: AuthCredentials) {
    return this.http.post<LoginResponse>(`${this.authUrl}/login`, credentials);
  }

  me() {
    return this.http.get<MeResponse>(`${this.authUrl}/me`);
  }
}
