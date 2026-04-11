import { HttpClient, HttpParams } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';

import { environment } from '../../../../environments/environment';
import {
  ActiveTransferDto,
  BranchPerformanceDto,
  DashboardResponseDto,
  DemandSummaryDto,
  InventoryAlertDto,
  SalesSummaryDto
} from './dtos/dashboard.dto';

@Injectable({
  providedIn: 'root'
})
export class DashboardApiService {
  private readonly http = inject(HttpClient);
  private readonly dashboardUrl = `${environment.apiBaseUrl}/dashboard`;

  getSalesSummary(idSucursal?: number | null) {
    return this.http.get<DashboardResponseDto<SalesSummaryDto>>(
      `${this.dashboardUrl}/volumen_ventas`,
      this.withBranchParams(idSucursal)
    );
  }

  getDemandSummary(idSucursal?: number | null) {
    return this.http.get<DashboardResponseDto<DemandSummaryDto>>(
      `${this.dashboardUrl}/rotacion_demanda`,
      this.withBranchParams(idSucursal)
    );
  }

  getActiveTransfers(idSucursal?: number | null) {
    return this.http.get<DashboardResponseDto<ActiveTransferDto[]>>(
      `${this.dashboardUrl}/transferencias_activas`,
      this.withBranchParams(idSucursal)
    );
  }

  getRestockAlerts(idSucursal?: number | null) {
    return this.http.get<DashboardResponseDto<InventoryAlertDto[]>>(
      `${this.dashboardUrl}/reabastecimiento`,
      this.withBranchParams(idSucursal)
    );
  }

  getBranchPerformance() {
    return this.http.get<DashboardResponseDto<BranchPerformanceDto[]>>(
      `${this.dashboardUrl}/rendimiento_sucursales`
    );
  }

  private withBranchParams(idSucursal?: number | null) {
    const params = idSucursal ? new HttpParams().set('id_sucursal', idSucursal) : undefined;
    return params ? { params } : {};
  }
}
