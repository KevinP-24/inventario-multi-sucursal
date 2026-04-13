import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';

import { environment } from '../../../../environments/environment';
import { ApiResponseDto } from '../../models/api-response.dto';
import { GuardarTransportistaDto, TransportistaDto } from './dtos/transportista.dto';

@Injectable({
  providedIn: 'root'
})
export class TransportistasApiService {
  private readonly http = inject(HttpClient);
  private readonly transportistasUrl = `${environment.apiBaseUrl}/transportistas`;

  listarTransportistas() {
    return this.http.get<ApiResponseDto<TransportistaDto[]>>(
      `${this.transportistasUrl}/listar_transportistas`
    );
  }

  obtenerTransportista(idTransportista: number) {
    return this.http.get<ApiResponseDto<TransportistaDto>>(
      `${this.transportistasUrl}/obtener_transportista/${idTransportista}`
    );
  }

  crearTransportista(payload: GuardarTransportistaDto) {
    return this.http.post<ApiResponseDto<TransportistaDto>>(
      `${this.transportistasUrl}/crear_transportista`,
      payload
    );
  }

  actualizarTransportista(idTransportista: number, payload: GuardarTransportistaDto) {
    return this.http.put<ApiResponseDto<TransportistaDto>>(
      `${this.transportistasUrl}/actualizar_transportista/${idTransportista}`,
      payload
    );
  }
}
