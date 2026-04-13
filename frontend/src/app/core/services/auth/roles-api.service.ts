import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';

import { environment } from '../../../../environments/environment';
import { RoleResponseDto, RolesResponseDto } from './dtos/auth-response.dto';
import { SaveRoleDto } from './dtos/role.dto';

@Injectable({
  providedIn: 'root'
})
export class RolesApiService {
  private readonly http = inject(HttpClient);
  private readonly rolesUrl = `${environment.apiBaseUrl}/roles`;

  listarRoles() {
    return this.http.get<RolesResponseDto>(`${this.rolesUrl}/listar_roles`);
  }

  obtenerRol(idRol: number) {
    return this.http.get<RoleResponseDto>(`${this.rolesUrl}/obtener_rol/${idRol}`);
  }

  crearRol(payload: SaveRoleDto) {
    return this.http.post<RoleResponseDto>(`${this.rolesUrl}/crear_rol`, payload);
  }

  actualizarRol(idRol: number, payload: SaveRoleDto) {
    return this.http.put<RoleResponseDto>(`${this.rolesUrl}/actualizar_rol/${idRol}`, payload);
  }

  crearRolesBase() {
    return this.http.post<RolesResponseDto>(`${this.rolesUrl}/crear_roles_base`, {});
  }
}
