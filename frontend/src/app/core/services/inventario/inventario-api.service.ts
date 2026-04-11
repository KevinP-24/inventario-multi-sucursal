import { Injectable } from '@angular/core';

import { InventarioSucursalApiService } from './inventario-sucursal-api.service';
import { ListasPrecioApiService } from './listas-precio-api.service';
import { MovimientosInventarioApiService } from './movimientos-inventario-api.service';
import { PreciosProductoApiService } from './precios-producto-api.service';
import { ProductoUnidadesApiService } from './producto-unidades-api.service';
import { ProductosApiService } from './productos-api.service';
import { TiposMovimientoInventarioApiService } from './tipos-movimiento-inventario-api.service';
import { UnidadesMedidaApiService } from './unidades-medida-api.service';

@Injectable({
  providedIn: 'root'
})
export class InventarioApiService {
  constructor(
    readonly inventarioSucursal: InventarioSucursalApiService,
    readonly productos: ProductosApiService,
    readonly movimientosInventario: MovimientosInventarioApiService,
    readonly listasPrecio: ListasPrecioApiService,
    readonly preciosProducto: PreciosProductoApiService,
    readonly productoUnidades: ProductoUnidadesApiService,
    readonly tiposMovimientoInventario: TiposMovimientoInventarioApiService,
    readonly unidadesMedida: UnidadesMedidaApiService
  ) {}
}
