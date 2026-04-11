export interface EnvioTransferenciaDto {
  readonly id_envio: number;
  readonly id_transferencia: number;
  readonly id_ruta: number;
  readonly id_transportista: number;
  readonly fecha_envio: string | null;
  readonly fecha_estimada_llegada: string | null;
  readonly fecha_real_llegada: string | null;
  readonly estado_envio: string;
}
