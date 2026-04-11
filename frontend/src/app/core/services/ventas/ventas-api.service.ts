import { Injectable } from '@angular/core';

import { ClientesApiService } from './clientes-api.service';
import { DetallesVentaApiService } from './detalles-venta-api.service';
import { TiposDocumentoApiService } from './tipos-documento-api.service';
import { VentaApiService } from './venta-api.service';

@Injectable({
  providedIn: 'root'
})
export class VentasApiService {
  constructor(
    readonly venta: VentaApiService,
    readonly detallesVenta: DetallesVentaApiService,
    readonly clientes: ClientesApiService,
    readonly tiposDocumento: TiposDocumentoApiService
  ) {}
}
