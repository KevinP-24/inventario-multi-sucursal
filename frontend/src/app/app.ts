import { HttpClient } from '@angular/common/http';
import { Component, inject, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';

import { environment } from '../environments/environment';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App {
  private readonly http = inject(HttpClient);

  protected readonly apiStatus = signal('Verificando conexion con la API...');
  protected readonly apiStatusType = signal<'checking' | 'online' | 'offline'>('checking');

  constructor() {
    this.http.get<{ message: string }>(`${environment.apiBaseUrl}/health/`).subscribe({
      next: (response) => {
        this.apiStatus.set(response.message);
        this.apiStatusType.set('online');
      },
      error: () => {
        this.apiStatus.set('API no disponible. Levanta el backend con Docker Compose.');
        this.apiStatusType.set('offline');
      },
    });
  }
}
