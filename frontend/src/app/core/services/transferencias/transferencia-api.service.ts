import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';

import { environment } from '../../../../environments/environment';
import { ApiResponseDto } from '../../models/api-response.dto';
import {
  ConfirmarRecepcionTransferenciaResultadoDto,
  CrearTransferenciaDto,
  RegistrarEnvioTransferenciaDto,
  RegistrarEnvioTransferenciaResultadoDto,
  RevisarTransferenciaDto,
  TransferenciaDto
} from './dtos/transferencia.dto';
import { ConfirmarRecepcionTransferenciaDto } from './dtos/recepcion-transferencia.dto';

@Injectable({
  providedIn: 'root'
})
export class TransferenciaApiService {
  private readonly http = inject(HttpClient);
  private readonly transferenciasUrl = `${environment.apiBaseUrl}/transferencias`;

  listarTransferencias() {
    return this.http.get<ApiResponseDto<TransferenciaDto[]>>(
      `${this.transferenciasUrl}/listar_transferencias`
    );
  }

  obtenerTransferencia(idTransferencia: number) {
    return this.http.get<ApiResponseDto<TransferenciaDto>>(
      `${this.transferenciasUrl}/obtener_transferencia/${idTransferencia}`
    );
  }

  crearTransferencia(payload: CrearTransferenciaDto) {
    return this.http.post<ApiResponseDto<TransferenciaDto>>(
      `${this.transferenciasUrl}/crear_transferencia`,
      payload
    );
  }

  revisarTransferencia(idTransferencia: number, payload: RevisarTransferenciaDto) {
    return this.http.post<ApiResponseDto<TransferenciaDto>>(
      `${this.transferenciasUrl}/revisar_transferencia/${idTransferencia}`,
      payload
    );
  }

  registrarEnvioTransferencia(
    idTransferencia: number,
    payload: RegistrarEnvioTransferenciaDto
  ) {
    return this.http.post<ApiResponseDto<RegistrarEnvioTransferenciaResultadoDto>>(
      `${this.transferenciasUrl}/registrar_envio_transferencia/${idTransferencia}`,
      payload
    );
  }

  confirmarRecepcionTransferencia(
    idTransferencia: number,
    payload: ConfirmarRecepcionTransferenciaDto
  ) {
    return this.http.post<ApiResponseDto<ConfirmarRecepcionTransferenciaResultadoDto>>(
      `${this.transferenciasUrl}/confirmar_recepcion_transferencia/${idTransferencia}`,
      payload
    );
  }
}
