import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';

import { environment } from '../../../../environments/environment';
import { ApiResponseDto } from '../../models/api-response.dto';
import { GuardarProductoUnidadDto, ProductoUnidadDto } from './dtos/producto-unidad.dto';

@Injectable({
  providedIn: 'root'
})
export class ProductoUnidadesApiService {
  private readonly http = inject(HttpClient);
  private readonly productoUnidadesUrl = `${environment.apiBaseUrl}/producto-unidades`;

  listarProductoUnidades() {
    return this.http.get<ApiResponseDto<ProductoUnidadDto[]>>(
      `${this.productoUnidadesUrl}/listar_producto_unidades`
    );
  }

  obtenerProductoUnidad(idProductoUnidad: number) {
    return this.http.get<ApiResponseDto<ProductoUnidadDto>>(
      `${this.productoUnidadesUrl}/obtener_producto_unidad/${idProductoUnidad}`
    );
  }

  crearProductoUnidad(payload: GuardarProductoUnidadDto) {
    return this.http.post<ApiResponseDto<ProductoUnidadDto>>(
      `${this.productoUnidadesUrl}/crear_producto_unidad`,
      payload
    );
  }

  actualizarProductoUnidad(idProductoUnidad: number, payload: GuardarProductoUnidadDto) {
    return this.http.put<ApiResponseDto<ProductoUnidadDto>>(
      `${this.productoUnidadesUrl}/actualizar_producto_unidad/${idProductoUnidad}`,
      payload
    );
  }

  eliminarProductoUnidad(idProductoUnidad: number) {
    return this.http.delete<ApiResponseDto<ProductoUnidadDto>>(
      `${this.productoUnidadesUrl}/eliminar_producto_unidad/${idProductoUnidad}`
    );
  }
}
