import { ChangeDetectionStrategy, Component } from '@angular/core';

import { PageHeaderComponent } from '../../shared/components/page-header/page-header.component';

@Component({
  selector: 'app-inventario-page',
  imports: [PageHeaderComponent],
  templateUrl: './inventario.page.html',
  styleUrl: './inventario.page.css',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class InventarioPage {}
