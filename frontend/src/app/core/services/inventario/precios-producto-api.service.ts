import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';

import { environment } from '../../../../environments/environment';
import { ApiResponseDto } from '../../models/api-response.dto';
import { GuardarPrecioProductoDto, PrecioProductoDto } from './dtos/precio-producto.dto';

@Injectable({
  providedIn: 'root'
})
export class PreciosProductoApiService {
  private readonly http = inject(HttpClient);
  private readonly preciosProductoUrl = `${environment.apiBaseUrl}/precios-producto`;

  listarPreciosProducto() {
    return this.http.get<ApiResponseDto<PrecioProductoDto[]>>(
      `${this.preciosProductoUrl}/listar_precios_producto`
    );
  }

  obtenerPrecioProducto(idPrecioProducto: number) {
    return this.http.get<ApiResponseDto<PrecioProductoDto>>(
      `${this.preciosProductoUrl}/obtener_precio_producto/${idPrecioProducto}`
    );
  }

  crearPrecioProducto(payload: GuardarPrecioProductoDto) {
    return this.http.post<ApiResponseDto<PrecioProductoDto>>(
      `${this.preciosProductoUrl}/crear_precio_producto`,
      payload
    );
  }

  actualizarPrecioProducto(idPrecioProducto: number, payload: GuardarPrecioProductoDto) {
    return this.http.put<ApiResponseDto<PrecioProductoDto>>(
      `${this.preciosProductoUrl}/actualizar_precio_producto/${idPrecioProducto}`,
      payload
    );
  }
}
