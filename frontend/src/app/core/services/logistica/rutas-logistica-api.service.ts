import { HttpClient, HttpParams } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';

import { environment } from '../../../../environments/environment';
import { ApiResponseDto } from '../../models/api-response.dto';
import {
  CriterioClasificacionRutaLogisticaDto,
  GuardarRutaLogisticaDto,
  RutaLogisticaDto
} from './dtos/ruta-logistica.dto';

@Injectable({
  providedIn: 'root'
})
export class RutasLogisticaApiService {
  private readonly http = inject(HttpClient);
  private readonly rutasLogisticaUrl = `${environment.apiBaseUrl}/rutas-logistica`;

  listarRutasLogistica() {
    return this.http.get<ApiResponseDto<RutaLogisticaDto[]>>(
      `${this.rutasLogisticaUrl}/listar_rutas_logistica`
    );
  }

  clasificarRutasLogistica(criterio?: CriterioClasificacionRutaLogisticaDto) {
    const params = criterio ? new HttpParams().set('criterio', criterio) : undefined;

    return this.http.get<ApiResponseDto<RutaLogisticaDto[]>>(
      `${this.rutasLogisticaUrl}/clasificar_rutas_logistica`,
      params ? { params } : {}
    );
  }

  reporteCumplimientoLogistico(idSucursal?: number | null, idRuta?: number | null) {
    let params = new HttpParams();

    if (idSucursal) {
      params = params.set('id_sucursal', idSucursal);
    }

    if (idRuta) {
      params = params.set('id_ruta', idRuta);
    }

    return this.http.get<ApiResponseDto<Record<string, unknown>[]>>(
      `${this.rutasLogisticaUrl}/reporte_cumplimiento_logistico`,
      { params }
    );
  }

  obtenerRutaLogistica(idRuta: number) {
    return this.http.get<ApiResponseDto<RutaLogisticaDto>>(
      `${this.rutasLogisticaUrl}/obtener_ruta_logistica/${idRuta}`
    );
  }

  crearRutaLogistica(payload: GuardarRutaLogisticaDto) {
    return this.http.post<ApiResponseDto<RutaLogisticaDto>>(
      `${this.rutasLogisticaUrl}/crear_ruta_logistica`,
      payload
    );
  }

  actualizarRutaLogistica(idRuta: number, payload: GuardarRutaLogisticaDto) {
    return this.http.put<ApiResponseDto<RutaLogisticaDto>>(
      `${this.rutasLogisticaUrl}/actualizar_ruta_logistica/${idRuta}`,
      payload
    );
  }
}
