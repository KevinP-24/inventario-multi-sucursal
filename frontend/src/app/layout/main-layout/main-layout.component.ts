import { CommonModule } from '@angular/common';
import { ChangeDetectionStrategy, Component, computed, inject, signal } from '@angular/core';
import { toSignal } from '@angular/core/rxjs-interop';
import { NavigationEnd, Router, RouterLink, RouterLinkActive, RouterOutlet } from '@angular/router';
import { filter, map, startWith } from 'rxjs';

import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import {
  faArrowRightFromBracket,
  faBars,
  faBoxesStacked,
  faChartLine,
  faChartPie,
  faGear,
  faHouse,
  faRightLeft,
  faShoppingBag,
  faStore,
  faTruck,
  faUser,
  faXmark
} from '@fortawesome/free-solid-svg-icons';
import { IconDefinition } from '@fortawesome/fontawesome-svg-core';

import { getNavigationItemsByRole } from '../../core/config/section-access.config';
import { ApiHealthService, ApiHealthState } from '../../core/services/api-health.service';
import { AuthSessionService } from '../../core/services/auth/auth-session.service';
import { StatusBadgeComponent } from '../../shared/components/status-badge/status-badge.component';

const initialApiState: ApiHealthState = {
  message: 'Verificando conexión con la API...',
  type: 'checking'
};

@Component({
  selector: 'app-main-layout',
  standalone: true,
  imports: [
    CommonModule,
    RouterLink,
    RouterLinkActive,
    RouterOutlet,
    StatusBadgeComponent,
    FontAwesomeModule
  ],
  templateUrl: './main-layout.component.html',
  styleUrl: './main-layout.component.css',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class MainLayoutComponent {
  private readonly router = inject(Router);
  private readonly apiHealthService = inject(ApiHealthService);
  private readonly authSession = inject(AuthSessionService);

  protected readonly currentUser = this.authSession.currentUser;
  protected readonly isSidebarOpen = signal(false);

  protected readonly apiState = toSignal(this.apiHealthService.checkHealth(), {
    initialValue: initialApiState
  });

  protected readonly resolvedRole = computed(() => {
    const user = this.currentUser();

    const roleCode = user?.rol?.codigo?.trim?.().toUpperCase?.();
    if (roleCode) {
      return roleCode;
    }

    const roleName = user?.rol?.nombre?.trim?.().toLowerCase?.();

    if (roleName === 'administrador general') {
      return 'ADMIN_GENERAL';
    }

    if (roleName === 'administrador de sucursal' || roleName === 'admin sucursal') {
      return 'ADMIN_SUCURSAL';
    }

    if (roleName === 'operario de inventario' || roleName === 'operador de inventario') {
      return 'OPERARIO_INVENTARIO';
    }

    const roleId = user?.id_rol ?? user?.rol?.id_rol ?? null;

    if (roleId === 1) {
      return 'ADMIN_GENERAL';
    }

    if (roleId === 2) {
      return 'ADMIN_SUCURSAL';
    }

    if (roleId === 3) {
      return 'OPERARIO_INVENTARIO';
    }

    return null;
  });

  protected readonly navigationItems = computed(() =>
    getNavigationItemsByRole(this.resolvedRole())
  );

  constructor() {
    console.log('USER', this.currentUser?.());
    console.log('ROLE RESOLVED', this.resolvedRole());
    console.log('NAV ITEMS', this.navigationItems());
  }
  private readonly currentUrl = toSignal(
    this.router.events.pipe(
      filter((event): event is NavigationEnd => event instanceof NavigationEnd),
      map((event) => event.urlAfterRedirects),
      startWith(this.router.url || '/app/dashboard')
    ),
    {
      initialValue: this.router.url || '/app/dashboard'
    }
  );

  protected readonly activeItem = computed(
    () =>
      this.navigationItems().find((item) => this.currentUrl().startsWith(item.path)) ??
      this.navigationItems()[0] ??
      null
  );

  protected readonly activeSection = computed(() => this.activeItem()?.label ?? 'Dashboard');

  protected readonly activeSectionDescription = computed(
    () => this.activeItem()?.description ?? 'Base lista para navegar por módulos del sistema.'
  );

  protected readonly userInitials = computed(() => {
    const name = this.currentUser()?.nombre?.trim() ?? '';

    if (!name) {
      return 'US';
    }

    const parts = name.split(/\s+/).filter(Boolean);
    const first = parts[0]?.[0] ?? '';
    const second = parts[1]?.[0] ?? '';

    return `${first}${second}`.toUpperCase();
  });

  protected readonly userIcon = faUser;
  protected readonly logoutIcon = faArrowRightFromBracket;
  protected readonly menuIcon = faBars;
  protected readonly closeMenuIcon = faXmark;

  private readonly iconMap: Record<string, IconDefinition> = {
    dashboard: faHouse,
    inventario: faBoxesStacked,
    compras: faShoppingBag,
    ventas: faChartLine,
    transferencias: faRightLeft,
    logistica: faTruck,
    reportes: faChartPie,
    sucursales: faStore,
    administracion: faGear,
    admin: faGear
  };

  protected resolveIcon(icon: string | null | undefined): IconDefinition {
    if (!icon) {
      return faHouse;
    }

    return this.iconMap[icon] ?? faHouse;
  }

  protected toggleSidebar() {
    this.isSidebarOpen.update((value) => !value);
  }

  protected closeSidebar() {
    this.isSidebarOpen.set(false);
  }

  protected closeSidebarOnMobile() {
    if (window.innerWidth <= 980) {
      this.closeSidebar();
    }
  }

  protected logout() {
    this.authSession.logout();
    void this.router.navigate(['/login']);
  }
}
