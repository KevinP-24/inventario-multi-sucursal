import { ChangeDetectionStrategy, Component } from '@angular/core';

import { PageHeaderComponent } from '../../shared/components/page-header/page-header.component';

@Component({
  selector: 'app-compras-page',
  imports: [PageHeaderComponent],
  templateUrl: './compras.page.html',
  styleUrl: './compras.page.css',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class ComprasPage {}
