import { HttpClient, HttpParams } from '@angular/common/http';
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

  listarVentas(filtros?: { id_sucursal?: number; id_cliente?: number; fecha_inicio?: string; fecha_fin?: string }) {
    let params = new HttpParams();
    if (filtros?.id_sucursal) params = params.set('id_sucursal', filtros.id_sucursal);
    if (filtros?.id_cliente) params = params.set('id_cliente', filtros.id_cliente);
    if (filtros?.fecha_inicio) params = params.set('fecha_inicio', filtros.fecha_inicio);
    if (filtros?.fecha_fin) params = params.set('fecha_fin', filtros.fecha_fin);

    return this.http.get<ApiResponseDto<VentaDto[]>>(`${this.ventasUrl}/listar_ventas`, { params });
  }

  obtenerVenta(idVenta: number) {
    return this.http.get<ApiResponseDto<VentaDto>>(`${this.ventasUrl}/obtener_venta/${idVenta}`);
  }

  crearVenta(payload: CrearVentaDto) {
    return this.http.post<ApiResponseDto<VentaDto>>(`${this.ventasUrl}/crear_venta`, payload);
  }
}
