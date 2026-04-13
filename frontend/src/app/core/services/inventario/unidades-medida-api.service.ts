import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';

import { environment } from '../../../../environments/environment';
import { ApiResponseDto } from '../../models/api-response.dto';
import { GuardarUnidadMedidaDto, UnidadMedidaDto } from './dtos/unidad-medida.dto';

@Injectable({
  providedIn: 'root'
})
export class UnidadesMedidaApiService {
  private readonly http = inject(HttpClient);
  private readonly unidadesMedidaUrl = `${environment.apiBaseUrl}/unidades-medida`;

  listarUnidadesMedida() {
    return this.http.get<ApiResponseDto<UnidadMedidaDto[]>>(
      `${this.unidadesMedidaUrl}/listar_unidades_medida`
    );
  }

  obtenerUnidadMedida(idUnidad: number) {
    return this.http.get<ApiResponseDto<UnidadMedidaDto>>(
      `${this.unidadesMedidaUrl}/obtener_unidad_medida/${idUnidad}`
    );
  }

  crearUnidadMedida(payload: GuardarUnidadMedidaDto) {
    return this.http.post<ApiResponseDto<UnidadMedidaDto>>(
      `${this.unidadesMedidaUrl}/crear_unidad_medida`,
      payload
    );
  }

  actualizarUnidadMedida(idUnidad: number, payload: GuardarUnidadMedidaDto) {
    return this.http.put<ApiResponseDto<UnidadMedidaDto>>(
      `${this.unidadesMedidaUrl}/actualizar_unidad_medida/${idUnidad}`,
      payload
    );
  }
}
