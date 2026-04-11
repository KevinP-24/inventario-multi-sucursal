import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';

import { environment } from '../../../../environments/environment';
import { ApiResponseDto } from '../../models/api-response.dto';
import { GuardarSucursalDto, SucursalDto } from './dtos/sucursal.dto';

@Injectable({
  providedIn: 'root'
})
export class SucursalesApiService {
  private readonly http = inject(HttpClient);
  private readonly sucursalesUrl = `${environment.apiBaseUrl}/sucursales`;

  listarSucursales() {
    return this.http.get<ApiResponseDto<SucursalDto[]>>(
      `${this.sucursalesUrl}/listar_sucursales`
    );
  }

  obtenerSucursal(idSucursal: number) {
    return this.http.get<ApiResponseDto<SucursalDto>>(
      `${this.sucursalesUrl}/obtener_sucursal/${idSucursal}`
    );
  }

  crearSucursal(payload: GuardarSucursalDto) {
    return this.http.post<ApiResponseDto<SucursalDto>>(
      `${this.sucursalesUrl}/crear_sucursal`,
      payload
    );
  }

  actualizarSucursal(idSucursal: number, payload: GuardarSucursalDto) {
    return this.http.put<ApiResponseDto<SucursalDto>>(
      `${this.sucursalesUrl}/actualizar_sucursal/${idSucursal}`,
      payload
    );
  }
}
