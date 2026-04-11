import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';

import { environment } from '../../../../environments/environment';
import { ApiResponseDto } from '../../models/api-response.dto';
import { GuardarParametroSistemaDto, ParametroSistemaDto } from './dtos/parametro-sistema.dto';

@Injectable({
  providedIn: 'root'
})
export class AdminApiService {
  private readonly http = inject(HttpClient);
  private readonly parametrosSistemaUrl = `${environment.apiBaseUrl}/parametros-sistema`;

  listarParametrosSistema() {
    return this.http.get<ApiResponseDto<ParametroSistemaDto[]>>(
      `${this.parametrosSistemaUrl}/listar_parametros_sistema`
    );
  }

  obtenerParametroSistema(idParametro: number) {
    return this.http.get<ApiResponseDto<ParametroSistemaDto>>(
      `${this.parametrosSistemaUrl}/obtener_parametro_sistema/${idParametro}`
    );
  }

  crearParametroSistema(payload: GuardarParametroSistemaDto) {
    return this.http.post<ApiResponseDto<ParametroSistemaDto>>(
      `${this.parametrosSistemaUrl}/crear_parametro_sistema`,
      payload
    );
  }

  actualizarParametroSistema(idParametro: number, payload: GuardarParametroSistemaDto) {
    return this.http.put<ApiResponseDto<ParametroSistemaDto>>(
      `${this.parametrosSistemaUrl}/actualizar_parametro_sistema/${idParametro}`,
      payload
    );
  }
}
