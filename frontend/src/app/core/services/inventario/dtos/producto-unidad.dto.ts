import { ProductoDto } from './producto.dto';
import { UnidadMedidaDto } from './unidad-medida.dto';

export interface ProductoUnidadDto {
  readonly id_producto_unidad: number;
  readonly id_producto: number;
  readonly id_unidad: number;
  readonly factor_conversion: number;
  readonly es_base: boolean;
  readonly activo: boolean;
  readonly producto: ProductoDto | null;
  readonly unidad_medida: UnidadMedidaDto | null;
}

export interface GuardarProductoUnidadDto {
  readonly id_producto: number;
  readonly id_unidad: number;
  readonly factor_conversion?: number;
  readonly es_base?: boolean;
}
