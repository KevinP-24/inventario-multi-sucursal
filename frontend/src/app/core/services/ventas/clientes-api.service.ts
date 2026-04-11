import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';

import { environment } from '../../../../environments/environment';
import { ApiResponseDto } from '../../models/api-response.dto';
import { ClienteDto, GuardarClienteDto } from './dtos/cliente.dto';

@Injectable({
  providedIn: 'root'
})
export class ClientesApiService {
  private readonly http = inject(HttpClient);
  private readonly clientesUrl = `${environment.apiBaseUrl}/clientes`;

  listarClientes() {
    return this.http.get<ApiResponseDto<ClienteDto[]>>(`${this.clientesUrl}/listar_clientes`);
  }

  obtenerCliente(idCliente: number) {
    return this.http.get<ApiResponseDto<ClienteDto>>(
      `${this.clientesUrl}/obtener_cliente/${idCliente}`
    );
  }

  crearCliente(payload: GuardarClienteDto) {
    return this.http.post<ApiResponseDto<ClienteDto>>(`${this.clientesUrl}/crear_cliente`, payload);
  }

  actualizarCliente(idCliente: number, payload: GuardarClienteDto) {
    return this.http.put<ApiResponseDto<ClienteDto>>(
      `${this.clientesUrl}/actualizar_cliente/${idCliente}`,
      payload
    );
  }
}
