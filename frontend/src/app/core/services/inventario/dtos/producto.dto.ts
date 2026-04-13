export interface ProductoDto {
  id_producto: number;
  codigo: string;
  nombre: string;
  descripcion: string | null;
  stock_minimo: number;
  activo: boolean;

  ultimo_costo_compra?: number | null;
  precio_venta_base?: number | null;
  costo_promedio_global?: number | null;
}

export interface GuardarProductoDto {
  codigo?: string;
  nombre?: string;
  descripcion?: string | null;
  stock_minimo?: number;
  activo?: boolean;
  precio_venta_base?: number | null;
}