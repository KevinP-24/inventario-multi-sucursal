import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';

import { ApiResponseDto } from '../../models/api-response.dto';
import { environment } from '../../../../environments/environment';
import { DetalleOrdenCompraDto } from './dtos/detalle-orden-compra.dto';

@Injectable({
  providedIn: 'root'
})
export class DetallesOrdenCompraApiService {
  private readonly http = inject(HttpClient);
  private readonly detallesOrdenCompraUrl = `${environment.apiBaseUrl}/detalles-orden-compra`;

  listarDetallesPorOrdenCompra(idOrdenCompra: number) {
    return this.http.get<ApiResponseDto<DetalleOrdenCompraDto[]>>(
      `${this.detallesOrdenCompraUrl}/listar_detalles_por_orden_compra/${idOrdenCompra}`
    );
  }
}
