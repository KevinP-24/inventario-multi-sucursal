import { ChangeDetectionStrategy, Component } from '@angular/core';

import { PageHeaderComponent } from '../../shared/components/page-header/page-header.component';

@Component({
  selector: 'app-reportes-page',
  imports: [PageHeaderComponent],
  templateUrl: './reportes.page.html',
  styleUrl: './reportes.page.css',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class ReportesPage {}
