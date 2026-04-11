import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';

import { environment } from '../../../../environments/environment';
import { ApiResponseDto } from '../../models/api-response.dto';
import { EstadoTransferenciaDto } from './dtos/estado-transferencia.dto';

@Injectable({
  providedIn: 'root'
})
export class EstadosTransferenciaApiService {
  private readonly http = inject(HttpClient);
  private readonly estadosTransferenciaUrl = `${environment.apiBaseUrl}/estados-transferencia`;

  listarEstadosTransferencia() {
    return this.http.get<ApiResponseDto<EstadoTransferenciaDto[]>>(
      `${this.estadosTransferenciaUrl}/listar_estados_transferencia`
    );
  }
}
