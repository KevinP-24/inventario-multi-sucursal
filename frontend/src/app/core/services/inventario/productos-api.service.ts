import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';

import { environment } from '../../../../environments/environment';
import { ApiResponseDto } from '../../models/api-response.dto';
import { GuardarProductoDto, ProductoDto } from './dtos/producto.dto';

@Injectable({
  providedIn: 'root'
})
export class ProductosApiService {
  private readonly http = inject(HttpClient);
  private readonly productosUrl = `${environment.apiBaseUrl}/productos`;

  listarProductos() {
    return this.http.get<ApiResponseDto<ProductoDto[]>>(`${this.productosUrl}/listar_productos`);
  }

  obtenerProducto(idProducto: number) {
    return this.http.get<ApiResponseDto<ProductoDto>>(
      `${this.productosUrl}/obtener_producto/${idProducto}`
    );
  }

  crearProducto(payload: GuardarProductoDto) {
    return this.http.post<ApiResponseDto<ProductoDto>>(
      `${this.productosUrl}/crear_producto`,
      payload
    );
  }

  actualizarProducto(idProducto: number, payload: GuardarProductoDto) {
    return this.http.put<ApiResponseDto<ProductoDto>>(
      `${this.productosUrl}/actualizar_producto/${idProducto}`,
      payload
    );
  }

  eliminarProducto(idProducto: number) {
    return this.http.delete<ApiResponseDto<ProductoDto>>(
      `${this.productosUrl}/eliminar_producto/${idProducto}`
    );
  }
}
