import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';

import { environment } from '../../../../environments/environment';
import { UserResponseDto, UsersResponseDto } from './dtos/auth-response.dto';
import { SaveUserDto } from './dtos/user.dto';

@Injectable({
  providedIn: 'root'
})
export class UsuariosApiService {
  private readonly http = inject(HttpClient);
  private readonly usersUrl = `${environment.apiBaseUrl}/usuarios`;

  listarUsuarios() {
    return this.http.get<UsersResponseDto>(`${this.usersUrl}/listar_usuarios`);
  }

  obtenerUsuario(idUsuario: number) {
    return this.http.get<UserResponseDto>(`${this.usersUrl}/obtener_usuario/${idUsuario}`);
  }

  crearUsuario(payload: SaveUserDto) {
    return this.http.post<UserResponseDto>(`${this.usersUrl}/crear_usuario`, payload);
  }

  actualizarUsuario(idUsuario: number, payload: SaveUserDto) {
    return this.http.put<UserResponseDto>(
      `${this.usersUrl}/actualizar_usuario/${idUsuario}`,
      payload
    );
  }
}
