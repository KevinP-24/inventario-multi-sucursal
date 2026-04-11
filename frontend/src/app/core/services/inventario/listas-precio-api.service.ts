import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';

import { environment } from '../../../../environments/environment';
import { ApiResponseDto } from '../../models/api-response.dto';
import { GuardarListaPrecioDto, ListaPrecioDto } from './dtos/lista-precio.dto';

@Injectable({
  providedIn: 'root'
})
export class ListasPrecioApiService {
  private readonly http = inject(HttpClient);
  private readonly listasPrecioUrl = `${environment.apiBaseUrl}/listas-precio`;

  listarListasPrecio() {
    return this.http.get<ApiResponseDto<ListaPrecioDto[]>>(
      `${this.listasPrecioUrl}/listar_listas_precio`
    );
  }

  obtenerListaPrecio(idListaPrecio: number) {
    return this.http.get<ApiResponseDto<ListaPrecioDto>>(
      `${this.listasPrecioUrl}/obtener_lista_precio/${idListaPrecio}`
    );
  }

  crearListaPrecio(payload: GuardarListaPrecioDto) {
    return this.http.post<ApiResponseDto<ListaPrecioDto>>(
      `${this.listasPrecioUrl}/crear_lista_precio`,
      payload
    );
  }

  actualizarListaPrecio(idListaPrecio: number, payload: GuardarListaPrecioDto) {
    return this.http.put<ApiResponseDto<ListaPrecioDto>>(
      `${this.listasPrecioUrl}/actualizar_lista_precio/${idListaPrecio}`,
      payload
    );
  }
}
