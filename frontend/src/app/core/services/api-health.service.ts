import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { catchError, map, of } from 'rxjs';

import { environment } from '../../../environments/environment';

export interface ApiHealthState {
  readonly message: string;
  readonly type: 'checking' | 'online' | 'offline';
}

@Injectable({
  providedIn: 'root'
})
export class ApiHealthService {
  private readonly http = inject(HttpClient);

  checkHealth() {
    return this.http.get<{ message: string }>(`${environment.apiBaseUrl}/health/`).pipe(
      map(
        (response): ApiHealthState => ({
        message: response.message,
        type: 'online' as const
        })
      ),
      catchError(() =>
        of<ApiHealthState>({
          message: 'API no disponible. Levanta el backend con Docker Compose.',
          type: 'offline' as const
        })
      )
    );
  }
}
