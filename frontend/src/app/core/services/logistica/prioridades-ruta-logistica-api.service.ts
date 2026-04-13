import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';

import { environment } from '../../../../environments/environment';
import { ApiResponseDto } from '../../models/api-response.dto';
import { PrioridadRutaLogisticaDto } from './dtos/prioridad-ruta-logistica.dto';

@Injectable({
  providedIn: 'root'
})
export class PrioridadesRutaLogisticaApiService {
  private readonly http = inject(HttpClient);
  private readonly prioridadesRutaLogisticaUrl =
    `${environment.apiBaseUrl}/prioridades-ruta-logistica`;

  listarPrioridadesRutaLogistica() {
    return this.http.get<ApiResponseDto<PrioridadRutaLogisticaDto[]>>(
      `${this.prioridadesRutaLogisticaUrl}/listar_prioridades_ruta_logistica`
    );
  }
}
