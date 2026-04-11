import { Injectable } from '@angular/core';

import { DetallesTransferenciaApiService } from './detalles-transferencia-api.service';
import { EstadosTransferenciaApiService } from './estados-transferencia-api.service';
import { TransferenciaApiService } from './transferencia-api.service';

@Injectable({
  providedIn: 'root'
})
export class TransferenciasApiService {
  constructor(
    readonly transferencia: TransferenciaApiService,
    readonly detallesTransferencia: DetallesTransferenciaApiService,
    readonly estadosTransferencia: EstadosTransferenciaApiService
  ) {}
}
