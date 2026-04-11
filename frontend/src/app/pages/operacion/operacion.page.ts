import { CommonModule, DatePipe, DecimalPipe } from '@angular/common';
import { ChangeDetectionStrategy, Component, computed, inject, signal } from '@angular/core';
import { forkJoin } from 'rxjs';

import { AuthSessionService } from '../../core/services/auth/auth-session.service';
import { UserRoleDto } from '../../core/services/auth/dtos/user-role.dto';
import { DashboardApiService } from '../../core/services/dashboard/dashboard-api.service';
import {
  ActiveTransferDto,
  DemandSummaryDto,
  InventoryAlertDto
} from '../../core/services/dashboard/dtos/dashboard.dto';
import { PageHeaderComponent } from '../../shared/components/page-header/page-header.component';

interface OperationRoleExperience {
  readonly eyebrow: string;
  readonly titlePrefix: string;
  readonly description: string;
  readonly focusTitle: string;
  readonly focusDescription: string;
  readonly focusPoints: readonly string[];
}

const OPERATION_ROLE_EXPERIENCE: Record<UserRoleDto, OperationRoleExperience> = {
  [UserRoleDto.ADMIN_GENERAL]: {
    eyebrow: 'Centro de operacion',
    titlePrefix: 'Panorama operativo de',
    description:
      'Vista consolidada para supervisar abastecimiento, transferencias y demanda sin depender de una pantalla por cada rol.',
    focusTitle: 'Enfoque de administracion general',
    focusDescription: 'Lectura transversal para toma de decisiones y seguimiento entre sucursales.',
    focusPoints: [
      'Detectar alertas de stock que requieran coordinacion central.',
      'Revisar transferencias activas con impacto entre sucursales.',
      'Priorizar referencias de alta rotacion para abastecimiento.'
    ]
  },
  [UserRoleDto.ADMIN_SUCURSAL]: {
    eyebrow: 'Centro de operacion',
    titlePrefix: 'Prioridades operativas de',
    description:
      'Resumen para coordinar abastecimiento, seguimiento de movimientos internos y demanda de la sucursal actual.',
    focusTitle: 'Enfoque de administracion de sucursal',
    focusDescription: 'Herramienta de seguimiento para ejecutar y destrabar la operacion diaria.',
    focusPoints: [
      'Validar productos agotados o por debajo del minimo.',
      'Dar seguimiento a solicitudes y recepciones pendientes.',
      'Anticipar reposicion con base en referencias de mayor salida.'
    ]
  },
  [UserRoleDto.OPERARIO_INVENTARIO]: {
    eyebrow: 'Centro de operacion',
    titlePrefix: 'Tareas operativas de',
    description:
      'Panel de trabajo para atender primero lo urgente en inventario, movimientos internos y productos de mayor rotacion.',
    focusTitle: 'Enfoque de operacion en piso',
    focusDescription: 'Vista orientada a ejecucion para el equipo que opera la sucursal.',
    focusPoints: [
      'Revisar productos agotados o bajo minimo.',
      'Dar seguimiento a transferencias con pendiente de despacho o recepcion.',
      'Identificar referencias de alta rotacion para anticipar reposicion.'
    ]
  }
};

@Component({
  selector: 'app-operacion-page',
  standalone: true,
  imports: [CommonModule, PageHeaderComponent, DecimalPipe, DatePipe],
  templateUrl: './operacion.page.html',
  styleUrl: './operacion.page.css',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class OperacionPage {
  private readonly authSession = inject(AuthSessionService);
  private readonly dashboardApi = inject(DashboardApiService);

  protected readonly currentUser = this.authSession.currentUser;
  protected readonly isLoading = signal(true);
  protected readonly loadError = signal<string | null>(null);
  protected readonly restockAlerts = signal<InventoryAlertDto[]>([]);
  protected readonly activeTransfers = signal<ActiveTransferDto[]>([]);
  protected readonly demandSummary = signal<DemandSummaryDto | null>(null);

  protected readonly branchName = computed(
    () => this.currentUser()?.sucursal?.nombre ?? 'tu sucursal'
  );
  protected readonly roleCode = computed(
    () => this.currentUser()?.rol?.codigo ?? UserRoleDto.OPERARIO_INVENTARIO
  );
  protected readonly roleName = computed(
    () => this.currentUser()?.rol?.nombre ?? 'Perfil operativo'
  );
  protected readonly operationExperience = computed(
    () => OPERATION_ROLE_EXPERIENCE[this.roleCode()] ?? OPERATION_ROLE_EXPERIENCE[UserRoleDto.OPERARIO_INVENTARIO]
  );
  protected readonly pageTitle = computed(
    () => `${this.operationExperience().titlePrefix} ${this.branchName()}`
  );
  protected readonly quickNotes = computed(() => [
    `Perfil activo: ${this.roleName()}`,
    `Sucursal: ${this.branchName()}`,
    `Transferencias abiertas: ${this.activeTransfers().length}`
  ]);

  constructor() {
    const branchId = this.currentUser()?.id_sucursal ?? null;

    forkJoin({
      restockAlerts: this.dashboardApi.getRestockAlerts(branchId),
      activeTransfers: this.dashboardApi.getActiveTransfers(branchId),
      demandSummary: this.dashboardApi.getDemandSummary(branchId)
    }).subscribe({
      next: (response) => {
        this.restockAlerts.set(response.restockAlerts.data);
        this.activeTransfers.set(response.activeTransfers.data);
        this.demandSummary.set(response.demandSummary.data);
        this.isLoading.set(false);
      },
      error: () => {
        this.loadError.set('No se pudo cargar el panel operativo de la sucursal.');
        this.isLoading.set(false);
      }
    });
  }
}
