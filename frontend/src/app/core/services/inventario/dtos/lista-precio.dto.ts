export interface ListaPrecioDto {
  readonly id_lista_precio: number;
  readonly nombre: string;
  readonly descripcion: string | null;
  readonly activa: boolean;
}

export interface GuardarListaPrecioDto {
  readonly nombre: string;
  readonly descripcion?: string | null;
  readonly activa?: boolean;
}
