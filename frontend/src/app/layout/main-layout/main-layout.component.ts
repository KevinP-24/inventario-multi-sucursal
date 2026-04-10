import { CommonModule } from '@angular/common';
import { ChangeDetectionStrategy, Component, computed, inject } from '@angular/core';
import { toSignal } from '@angular/core/rxjs-interop';
import { NavigationEnd, Router, RouterLink, RouterLinkActive, RouterOutlet } from '@angular/router';
import { filter, map, startWith } from 'rxjs';

import { navigationItems } from '../../core/data/navigation.data';
import { ApiHealthService, ApiHealthState } from '../../core/services/api-health.service';
import { AuthSessionService } from '../../core/services/auth/auth-session.service';
import { StatusBadgeComponent } from '../../shared/components/status-badge/status-badge.component';

const initialApiState: ApiHealthState = {
  message: 'Verificando conexion con la API...',
  type: 'checking'
};

@Component({
  selector: 'app-main-layout',
  imports: [CommonModule, RouterLink, RouterLinkActive, RouterOutlet, StatusBadgeComponent],
  templateUrl: './main-layout.component.html',
  styleUrl: './main-layout.component.css',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class MainLayoutComponent {
  private readonly router = inject(Router);
  private readonly apiHealthService = inject(ApiHealthService);
  private readonly authSession = inject(AuthSessionService);

  protected readonly navigationItems = navigationItems;
  protected readonly currentUser = this.authSession.currentUser;
  protected readonly apiState = toSignal(this.apiHealthService.checkHealth(), { initialValue: initialApiState });

  private readonly currentUrl = toSignal(
    this.router.events.pipe(
      filter((event): event is NavigationEnd => event instanceof NavigationEnd),
      map((event) => event.urlAfterRedirects),
      startWith(this.router.url || '/app/dashboard')
    ),
    { initialValue: this.router.url || '/app/dashboard' }
  );

  protected readonly activeSection = computed(
    () =>
      this.navigationItems.find((item) => this.currentUrl().startsWith(item.path))?.label ?? 'Dashboard'
  );

  protected logout() {
    this.authSession.logout();
    void this.router.navigate(['/login']);
  }
}
