import { HttpClient, HttpParams } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';

import { environment } from '../../../../environments/environment';
import { ApiResponseDto } from '../../models/api-response.dto';
import {
  ActualizarInventarioSucursalDto,
  AjustarInventarioDto,
  CrearInventarioSucursalDto,
  InventarioMovimientoResultadoDto,
  InventarioSucursalDto,
  MovimientoOperativoInventarioDto,
  StockAlertDto
} from './dtos/inventario-sucursal.dto';

@Injectable({
  providedIn: 'root'
})
export class InventarioSucursalApiService {
  private readonly http = inject(HttpClient);
  private readonly inventarioSucursalUrl = `${environment.apiBaseUrl}/inventario-sucursal`;

  listarInventarioSucursal() {
    return this.http.get<ApiResponseDto<InventarioSucursalDto[]>>(
      `${this.inventarioSucursalUrl}/listar_inventario_sucursal`
    );
  }

  listarAlertasStockBajo(idSucursal?: number | null) {
    const params = idSucursal ? new HttpParams().set('id_sucursal', idSucursal) : undefined;

    return this.http.get<ApiResponseDto<StockAlertDto[]>>(
      `${this.inventarioSucursalUrl}/listar_alertas_stock_bajo`,
      params ? { params } : {}
    );
  }

  obtenerInventarioSucursal(idInventario: number) {
    return this.http.get<ApiResponseDto<InventarioSucursalDto>>(
      `${this.inventarioSucursalUrl}/obtener_inventario_sucursal/${idInventario}`
    );
  }

  crearInventarioSucursal(payload: CrearInventarioSucursalDto) {
    return this.http.post<ApiResponseDto<InventarioSucursalDto>>(
      `${this.inventarioSucursalUrl}/crear_inventario_sucursal`,
      payload
    );
  }

  actualizarInventarioSucursal(idInventario: number, payload: ActualizarInventarioSucursalDto) {
    return this.http.put<ApiResponseDto<InventarioSucursalDto>>(
      `${this.inventarioSucursalUrl}/actualizar_inventario_sucursal/${idInventario}`,
      payload
    );
  }

  ajustarInventarioSucursal(idInventario: number, payload: AjustarInventarioDto) {
    return this.http.post<ApiResponseDto<InventarioMovimientoResultadoDto>>(
      `${this.inventarioSucursalUrl}/ajustar_inventario_sucursal/${idInventario}`,
      payload
    );
  }

  registrarDevolucionInventario(
    idInventario: number,
    payload: MovimientoOperativoInventarioDto
  ) {
    return this.http.post<ApiResponseDto<InventarioMovimientoResultadoDto>>(
      `${this.inventarioSucursalUrl}/registrar_devolucion_inventario/${idInventario}`,
      payload
    );
  }

  registrarMermaInventario(idInventario: number, payload: MovimientoOperativoInventarioDto) {
    return this.http.post<ApiResponseDto<InventarioMovimientoResultadoDto>>(
      `${this.inventarioSucursalUrl}/registrar_merma_inventario/${idInventario}`,
      payload
    );
  }
}
