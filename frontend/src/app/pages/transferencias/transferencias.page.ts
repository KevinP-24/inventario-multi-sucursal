import { ChangeDetectionStrategy, Component } from '@angular/core';

import { PageHeaderComponent } from '../../shared/components/page-header/page-header.component';

@Component({
  selector: 'app-transferencias-page',
  imports: [PageHeaderComponent],
  templateUrl: './transferencias.page.html',
  styleUrl: './transferencias.page.css',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class TransferenciasPage {}
