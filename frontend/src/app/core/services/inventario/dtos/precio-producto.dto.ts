import { ListaPrecioDto } from './lista-precio.dto';
import { ProductoDto } from './producto.dto';

export interface PrecioProductoDto {
  readonly id_precio_producto: number;
  readonly id_producto: number;
  readonly id_lista_precio: number;
  readonly precio: number;
  readonly fecha_vigencia: string | null;
  readonly activo: boolean;
  readonly producto: ProductoDto | null;
  readonly lista_precio: ListaPrecioDto | null;
}

export interface GuardarPrecioProductoDto {
  readonly id_producto: number;
  readonly id_lista_precio: number;
  readonly precio: number;
  readonly fecha_vigencia?: string;
  readonly activo?: boolean;
}
