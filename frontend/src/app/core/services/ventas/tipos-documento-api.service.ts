import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';

import { environment } from '../../../../environments/environment';
import { ApiResponseDto } from '../../models/api-response.dto';
import { TipoDocumentoDto } from './dtos/tipo-documento.dto';

@Injectable({
  providedIn: 'root'
})
export class TiposDocumentoApiService {
  private readonly http = inject(HttpClient);
  private readonly tiposDocumentoUrl = `${environment.apiBaseUrl}/tipos-documento`;

  listarTiposDocumento() {
    return this.http.get<ApiResponseDto<TipoDocumentoDto[]>>(
      `${this.tiposDocumentoUrl}/listar_tipos_documento`
    );
  }
}
