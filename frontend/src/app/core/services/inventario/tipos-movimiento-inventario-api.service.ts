import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';

import { environment } from '../../../../environments/environment';
import { ApiResponseDto } from '../../models/api-response.dto';
import { TipoMovimientoInventarioDto } from './dtos/tipo-movimiento-inventario.dto';

@Injectable({
  providedIn: 'root'
})
export class TiposMovimientoInventarioApiService {
  private readonly http = inject(HttpClient);
  private readonly tiposMovimientoInventarioUrl =
    `${environment.apiBaseUrl}/tipos-movimiento-inventario`;

  listarTiposMovimientoInventario() {
    return this.http.get<ApiResponseDto<TipoMovimientoInventarioDto[]>>(
      `${this.tiposMovimientoInventarioUrl}/listar_tipos_movimiento_inventario`
    );
  }
}
