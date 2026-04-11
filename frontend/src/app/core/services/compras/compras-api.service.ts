import { Injectable } from '@angular/core';

import { DetallesOrdenCompraApiService } from './detalles-orden-compra-api.service';
import { OrdenesCompraApiService } from './ordenes-compra-api.service';
import { ProveedoresApiService } from './proveedores-api.service';

@Injectable({
  providedIn: 'root'
})
export class ComprasApiService {
  constructor(
    readonly ordenesCompra: OrdenesCompraApiService,
    readonly detallesOrdenCompra: DetallesOrdenCompraApiService,
    readonly proveedores: ProveedoresApiService
  ) {}
}
