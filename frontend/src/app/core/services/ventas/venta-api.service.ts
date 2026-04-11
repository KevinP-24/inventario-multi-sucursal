import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';

import { environment } from '../../../../environments/environment';
import { ApiResponseDto } from '../../models/api-response.dto';
import { CrearVentaDto, VentaDto } from './dtos/venta.dto';

@Injectable({
  providedIn: 'root'
})
export class VentaApiService {
  private readonly http = inject(HttpClient);
  private readonly ventasUrl = `${environment.apiBaseUrl}/ventas`;

  listarVentas() {
    return this.http.get<ApiResponseDto<VentaDto[]>>(`${this.ventasUrl}/listar_ventas`);
  }

  obtenerVenta(idVenta: number) {
    return this.http.get<ApiResponseDto<VentaDto>>(`${this.ventasUrl}/obtener_venta/${idVenta}`);
  }

  crearVenta(payload: CrearVentaDto) {
    return this.http.post<ApiResponseDto<VentaDto>>(`${this.ventasUrl}/crear_venta`, payload);
  }
}
