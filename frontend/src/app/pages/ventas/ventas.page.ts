import { ChangeDetectionStrategy, Component } from '@angular/core';

import { PageHeaderComponent } from '../../shared/components/page-header/page-header.component';

@Component({
  selector: 'app-ventas-page',
  imports: [PageHeaderComponent],
  templateUrl: './ventas.page.html',
  styleUrl: './ventas.page.css',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class VentasPage {}
