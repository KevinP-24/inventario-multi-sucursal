import { HttpClient, HttpParams } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';

import { ApiResponseDto } from '../../models/api-response.dto';
import { environment } from '../../../../environments/environment';
import {
  CrearOrdenCompraDto,
  HistorialComprasFiltrosDto,
  OrdenCompraDto,
  OrdenCompraRecepcionResultadoDto,
  RecibirOrdenCompraDto
} from './dtos/orden-compra.dto';

@Injectable({
  providedIn: 'root'
})
export class OrdenesCompraApiService {
  private readonly http = inject(HttpClient);
  private readonly ordenesCompraUrl = `${environment.apiBaseUrl}/ordenes-compra`;

  listarOrdenesCompra() {
    return this.http.get<ApiResponseDto<OrdenCompraDto[]>>(
      `${this.ordenesCompraUrl}/listar_ordenes_compra`
    );
  }

  obtenerOrdenCompra(idOrdenCompra: number) {
    return this.http.get<ApiResponseDto<OrdenCompraDto>>(
      `${this.ordenesCompraUrl}/obtener_orden_compra/${idOrdenCompra}`
    );
  }

  filtrarHistorialCompras(filtros: HistorialComprasFiltrosDto = {}) {
    let params = new HttpParams();

    Object.entries(filtros).forEach(([key, value]) => {
      if (value !== undefined && value !== null && value !== '') {
        params = params.set(key, String(value));
      }
    });

    return this.http.get<ApiResponseDto<OrdenCompraDto[]>>(
      `${this.ordenesCompraUrl}/filtrar_historial_compras`,
      { params }
    );
  }

  crearOrdenCompra(payload: CrearOrdenCompraDto) {
    return this.http.post<ApiResponseDto<OrdenCompraDto>>(
      `${this.ordenesCompraUrl}/crear_orden_compra`,
      payload
    );
  }

  anularOrdenCompra(idOrdenCompra: number) {
    return this.http.post<ApiResponseDto<OrdenCompraDto>>(
      `${this.ordenesCompraUrl}/anular_orden_compra/${idOrdenCompra}`,
      {}
    );
  }

  recibirOrdenCompra(idOrdenCompra: number, payload: RecibirOrdenCompraDto) {
    return this.http.post<ApiResponseDto<OrdenCompraRecepcionResultadoDto>>(
      `${this.ordenesCompraUrl}/recibir_orden_compra/${idOrdenCompra}`,
      payload
    );
  }
}
