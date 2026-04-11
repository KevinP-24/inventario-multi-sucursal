import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';

import { environment } from '../../../../environments/environment';
import { ApiResponseDto } from '../../models/api-response.dto';
import { DetalleTransferenciaDto } from './dtos/detalle-transferencia.dto';

@Injectable({
  providedIn: 'root'
})
export class DetallesTransferenciaApiService {
  private readonly http = inject(HttpClient);
  private readonly detallesTransferenciaUrl = `${environment.apiBaseUrl}/detalles-transferencia`;

  listarDetallesPorTransferencia(idTransferencia: number) {
    return this.http.get<ApiResponseDto<DetalleTransferenciaDto[]>>(
      `${this.detallesTransferenciaUrl}/listar_detalles_por_transferencia/${idTransferencia}`
    );
  }
}
