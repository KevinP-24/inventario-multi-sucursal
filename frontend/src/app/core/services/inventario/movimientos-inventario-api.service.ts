import { HttpClient, HttpParams } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';

import { environment } from '../../../../environments/environment';
import { ApiResponseDto } from '../../models/api-response.dto';
import {
  FiltrosMovimientoInventarioDto,
  MovimientoInventarioDto,
  RegistrarMovimientoInventarioDto
} from './dtos/movimiento-inventario.dto';

@Injectable({
  providedIn: 'root'
})
export class MovimientosInventarioApiService {
  private readonly http = inject(HttpClient);
  private readonly movimientosInventarioUrl = `${environment.apiBaseUrl}/movimientos-inventario`;

  listarMovimientosInventario() {
    return this.http.get<ApiResponseDto<MovimientoInventarioDto[]>>(
      `${this.movimientosInventarioUrl}/listar_movimientos_inventario`
    );
  }

  filtrarMovimientosInventario(filtros: FiltrosMovimientoInventarioDto = {}) {
    let params = new HttpParams();

    Object.entries(filtros).forEach(([key, value]) => {
      if (value !== undefined && value !== null && value !== '') {
        params = params.set(key, String(value));
      }
    });

    return this.http.get<ApiResponseDto<MovimientoInventarioDto[]>>(
      `${this.movimientosInventarioUrl}/filtrar_movimientos_inventario`,
      { params }
    );
  }

  obtenerMovimientoInventario(idMovimiento: number) {
    return this.http.get<ApiResponseDto<MovimientoInventarioDto>>(
      `${this.movimientosInventarioUrl}/obtener_movimiento_inventario/${idMovimiento}`
    );
  }

  listarMovimientosPorInventario(idInventario: number) {
    return this.http.get<ApiResponseDto<MovimientoInventarioDto[]>>(
      `${this.movimientosInventarioUrl}/listar_movimientos_por_inventario/${idInventario}`
    );
  }

  registrarMovimientoInventario(payload: RegistrarMovimientoInventarioDto) {
    return this.http.post<ApiResponseDto<MovimientoInventarioDto>>(
      `${this.movimientosInventarioUrl}/registrar_movimiento_inventario`,
      payload
    );
  }
}
