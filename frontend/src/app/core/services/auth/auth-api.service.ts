import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';

import { environment } from '../../../../environments/environment';
import { AuthCredentialsDto } from './dtos/auth-credentials.dto';
import { LoginResponseDto, MeResponseDto } from './dtos/auth-response.dto';

@Injectable({
  providedIn: 'root'
})
export class AuthApiService {
  private readonly http = inject(HttpClient);
  private readonly authUrl = `${environment.apiBaseUrl}/auth`;

  login(credentials: AuthCredentialsDto) {
    return this.http.post<LoginResponseDto>(`${this.authUrl}/login`, credentials);
  }

  me() {
    return this.http.get<MeResponseDto>(`${this.authUrl}/me`);
  }
}
