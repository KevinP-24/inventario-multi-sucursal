import { HttpClient, HttpParams } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';

import { environment } from '../../../../environments/environment';
import { ReporteFiltrosDto } from './dtos/reporte-filtros.dto';

@Injectable({
  providedIn: 'root'
})
export class ReportesApiService {
  private readonly http = inject(HttpClient);
  private readonly reportesUrl = `${environment.apiBaseUrl}/reportes`;

  exportarVentasPdf(filtros: ReporteFiltrosDto = {}) {
    return this.http.get(`${this.reportesUrl}/ventas/pdf`, {
      params: this.buildParams(filtros),
      responseType: 'blob'
    });
  }

  exportarInventarioPdf(filtros: ReporteFiltrosDto = {}) {
    return this.http.get(`${this.reportesUrl}/inventario/pdf`, {
      params: this.buildParams(filtros),
      responseType: 'blob'
    });
  }

  exportarTransferenciasPdf(filtros: ReporteFiltrosDto = {}) {
    return this.http.get(`${this.reportesUrl}/transferencias/pdf`, {
      params: this.buildParams(filtros),
      responseType: 'blob'
    });
  }

  private buildParams(filtros: ReporteFiltrosDto) {
    let params = new HttpParams();

    Object.entries(filtros).forEach(([key, value]) => {
      if (value !== undefined && value !== null && value !== '') {
        params = params.set(key, String(value));
      }
    });

    return params;
  }
}
