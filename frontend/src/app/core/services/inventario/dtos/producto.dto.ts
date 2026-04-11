export interface ProductoDto {
  readonly id_producto: number;
  readonly codigo: string;
  readonly nombre: string;
  readonly descripcion: string | null;
  readonly stock_minimo: number;
  readonly activo: boolean;
}

export interface GuardarProductoDto {
  readonly codigo: string;
  readonly nombre: string;
  readonly descripcion?: string | null;
  readonly stock_minimo?: number;
}
