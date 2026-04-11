import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';

import { ApiResponseDto } from '../../models/api-response.dto';
import { environment } from '../../../../environments/environment';
import { GuardarProveedorDto, ProveedorDto } from './dtos/proveedor.dto';

@Injectable({
  providedIn: 'root'
})
export class ProveedoresApiService {
  private readonly http = inject(HttpClient);
  private readonly proveedoresUrl = `${environment.apiBaseUrl}/proveedores`;

  listarProveedores() {
    return this.http.get<ApiResponseDto<ProveedorDto[]>>(
      `${this.proveedoresUrl}/listar_proveedores`
    );
  }

  obtenerProveedor(idProveedor: number) {
    return this.http.get<ApiResponseDto<ProveedorDto>>(
      `${this.proveedoresUrl}/obtener_proveedor/${idProveedor}`
    );
  }

  crearProveedor(payload: GuardarProveedorDto) {
    return this.http.post<ApiResponseDto<ProveedorDto>>(
      `${this.proveedoresUrl}/crear_proveedor`,
      payload
    );
  }

  actualizarProveedor(idProveedor: number, payload: GuardarProveedorDto) {
    return this.http.put<ApiResponseDto<ProveedorDto>>(
      `${this.proveedoresUrl}/actualizar_proveedor/${idProveedor}`,
      payload
    );
  }
}
