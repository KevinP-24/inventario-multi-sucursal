import { Injectable } from '@angular/core';

import { PrioridadesRutaLogisticaApiService } from './prioridades-ruta-logistica-api.service';
import { RutasLogisticaApiService } from './rutas-logistica-api.service';
import { TransportistasApiService } from './transportistas-api.service';

@Injectable({
  providedIn: 'root'
})
export class LogisticaApiService {
  constructor(
    readonly transportistas: TransportistasApiService,
    readonly prioridadesRutaLogistica: PrioridadesRutaLogisticaApiService,
    readonly rutasLogistica: RutasLogisticaApiService
  ) {}
}
