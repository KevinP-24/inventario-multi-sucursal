import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';

import { environment } from '../../../../environments/environment';
import { ApiResponseDto } from '../../models/api-response.dto';
import { DetalleVentaDto } from './dtos/detalle-venta.dto';

@Injectable({
  providedIn: 'root'
})
export class DetallesVentaApiService {
  private readonly http = inject(HttpClient);
  private readonly detallesVentaUrl = `${environment.apiBaseUrl}/detalles-venta`;

  listarDetallesPorVenta(idVenta: number) {
    return this.http.get<ApiResponseDto<DetalleVentaDto[]>>(
      `${this.detallesVentaUrl}/listar_detalles_por_venta/${idVenta}`
    );
  }
}
