import { ChangeDetectionStrategy, Component } from '@angular/core';

import { dashboardModules } from '../../core/data/dashboard.data';
import { PageHeaderComponent } from '../../shared/components/page-header/page-header.component';

@Component({
  selector: 'app-dashboard-page',
  imports: [PageHeaderComponent],
  templateUrl: './dashboard.page.html',
  styleUrl: './dashboard.page.css',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class DashboardPage {
  protected readonly modules = dashboardModules;
}
