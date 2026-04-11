import { CommonModule } from '@angular/common';
import { ChangeDetectionStrategy, Component, computed, inject } from '@angular/core';
import { RouterLink } from '@angular/router';

import { AuthSessionService } from '../../core/services/auth/auth-session.service';
import { PageHeaderComponent } from '../../shared/components/page-header/page-header.component';

type RoleCode = 'ADMIN_GENERAL' | 'ADMIN_SUCURSAL' | 'OPERARIO_INVENTARIO';

interface DashboardModuleCard {
  caption: string;
  title: string;
  description: string;
}

interface DashboardShortcut {
  label: string;
  route: string;
  description: string;
}

interface DashboardFocusItem {
  title: string;
  description: string;
}

interface DashboardViewModel {
  eyebrow: string;
  title: string;
  description: string;
  modules: DashboardModuleCard[];
  shortcuts: DashboardShortcut[];
  focus: DashboardFocusItem[];
}

const DASHBOARD_BY_ROLE: Record<RoleCode, DashboardViewModel> = {
  ADMIN_GENERAL: {
    eyebrow: 'Dashboard administrativo',
    title: 'Vision general de la operacion multi-sucursal',
    description:
      'Consolida accesos clave para supervision global, consulta transversal y seguimiento del estado general del sistema.',
    modules: [
      {
        caption: 'Control global',
        title: 'Inventario consolidado',
        description:
          'Consulta el comportamiento general del inventario y revisa la situacion por sucursal.'
      },
      {
        caption: 'Gestion central',
        title: 'Transferencias y abastecimiento',
        description:
          'Supervisa movimientos entre sucursales, estado logistico y posibles cuellos de operacion.'
      },
      {
        caption: 'Analitica',
        title: 'Indicadores y reportes',
        description:
          'Accede a resumenes de ventas, alertas y comparativas para apoyar decisiones.'
      }
    ],
    shortcuts: [
      {
        label: 'Dashboard operativo',
        route: '/app/operacion',
        description: 'Vista resumida de alertas y actividad prioritaria.'
      },
      {
        label: 'Inventario',
        route: '/app/inventario',
        description: 'Consulta existencias, movimientos y stock por sucursal.'
      },
      {
        label: 'Transferencias',
        route: '/app/transferencias',
        description: 'Revisa solicitudes, envios y recepciones.'
      },
      {
        label: 'Reportes',
        route: '/app/reportes',
        description: 'Accede a exportables y consultas consolidadas.'
      }
    ],
    focus: [
      {
        title: 'Supervision transversal',
        description: 'Ver el estado general de la red y detectar desbalances entre sucursales.'
      },
      {
        title: 'Seguimiento logistico',
        description: 'Controlar transferencias activas, pendientes y posibles retrasos.'
      },
      {
        title: 'Decision administrativa',
        description: 'Usar indicadores y reportes para priorizar abastecimiento y control.'
      }
    ]
  },
  ADMIN_SUCURSAL: {
    eyebrow: 'Dashboard de sucursal',
    title: 'Control operativo y administrativo de tu sucursal',
    description:
      'Prioriza el seguimiento de inventario, ventas, compras y transferencias con enfoque local.',
    modules: [
      {
        caption: 'Sucursal',
        title: 'Estado del inventario',
        description:
          'Consulta stock actual, referencias criticas y productos con necesidad de reabastecimiento.'
      },
      {
        caption: 'Seguimiento',
        title: 'Transferencias activas',
        description:
          'Valida movimientos en curso y revisa solicitudes relacionadas con tu sucursal.'
      },
      {
        caption: 'Gestion',
        title: 'Ventas y abastecimiento',
        description:
          'Haz seguimiento a la operacion comercial y a la reposicion de inventario.'
      }
    ],
    shortcuts: [
      {
        label: 'Inventario',
        route: '/app/inventario',
        description: 'Consulta stock, alertas y movimientos.'
      },
      {
        label: 'Compras',
        route: '/app/compras',
        description: 'Gestiona ordenes y recepciones.'
      },
      {
        label: 'Ventas',
        route: '/app/ventas',
        description: 'Consulta ventas y flujo comercial.'
      },
      {
        label: 'Transferencias',
        route: '/app/transferencias',
        description: 'Controla solicitudes, despachos y recepciones.'
      }
    ],
    focus: [
      {
        title: 'Control local',
        description: 'Mantener abastecida la sucursal y monitorear referencias criticas.'
      },
      {
        title: 'Seguimiento diario',
        description: 'Revisar transferencias, ventas y necesidades de reposicion.'
      },
      {
        title: 'Visibilidad operativa',
        description: 'Tener una base clara para tomar decisiones rapidas dentro de la sede.'
      }
    ]
  },
  OPERARIO_INVENTARIO: {
    eyebrow: 'Dashboard operativo',
    title: 'Acciones clave para la operacion del dia',
    description:
      'Centraliza accesos directos a las tareas que mas impactan el flujo diario de inventario.',
    modules: [
      {
        caption: 'Operacion',
        title: 'Inventario y movimientos',
        description:
          'Consulta existencias, registra novedades y mantén actualizada la trazabilidad operativa.'
      },
      {
        caption: 'Atencion inmediata',
        title: 'Transferencias activas',
        description:
          'Haz seguimiento a solicitudes, envios y recepciones que requieren accion.'
      },
      {
        caption: 'Ejecucion',
        title: 'Ventas y compras',
        description:
          'Accede a los modulos transaccionales necesarios para el movimiento diario.'
      }
    ],
    shortcuts: [
      {
        label: 'Panel operativo',
        route: '/app/operacion',
        description: 'Alertas, transferencias activas y prioridades inmediatas.'
      },
      {
        label: 'Inventario',
        route: '/app/inventario',
        description: 'Consulta y actualiza existencias.'
      },
      {
        label: 'Ventas',
        route: '/app/ventas',
        description: 'Registra y consulta ventas.'
      },
      {
        label: 'Transferencias',
        route: '/app/transferencias',
        description: 'Gestiona solicitudes y recepciones.'
      }
    ],
    focus: [
      {
        title: 'Reabastecimiento',
        description: 'Detectar productos agotados o bajo minimo para actuar rapido.'
      },
      {
        title: 'Transferencias',
        description: 'Dar continuidad a envios, recepciones y pendientes operativos.'
      },
      {
        title: 'Ejecucion diaria',
        description: 'Entrar directo a los modulos que sostienen la operacion de la sucursal.'
      }
    ]
  }
};

@Component({
  selector: 'app-dashboard-page',
  standalone: true,
  imports: [CommonModule, RouterLink, PageHeaderComponent],
  templateUrl: './dashboard.page.html',
  styleUrl: './dashboard.page.css',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class DashboardPage {
  private readonly authSession = inject(AuthSessionService);

  protected readonly currentUser = this.authSession.currentUser;

  protected readonly roleCode = computed<RoleCode>(() => {
    const role = this.currentUser()?.rol?.codigo;

    if (
      role === 'ADMIN_GENERAL' ||
      role === 'ADMIN_SUCURSAL' ||
      role === 'OPERARIO_INVENTARIO'
    ) {
      return role;
    }

    return 'OPERARIO_INVENTARIO';
  });

  protected readonly content = computed(() => DASHBOARD_BY_ROLE[this.roleCode()]);
}