import { CommonModule } from '@angular/common';
import { HttpErrorResponse } from '@angular/common/http';
import {
  ChangeDetectionStrategy,
  Component,
  DestroyRef,
  OnInit,
  computed,
  inject,
  signal
} from '@angular/core';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { finalize, forkJoin } from 'rxjs';

import { LogisticaApiService } from '../../core/services/logistica/logistica-api.service';
import { GuardarRutaLogisticaDto, RutaLogisticaDto } from '../../core/services/logistica/dtos/ruta-logistica.dto';
import {
  GuardarTransportistaDto,
  TransportistaDto
} from '../../core/services/logistica/dtos/transportista.dto';
import { PrioridadRutaLogisticaDto } from '../../core/services/logistica/dtos/prioridad-ruta-logistica.dto';
import { SucursalDto } from '../../core/services/sucursales/dtos/sucursal.dto';
import { SucursalesApiService } from '../../core/services/sucursales/sucursales-api.service';
import { TransferenciasApiService } from '../../core/services/transferencias/transferencias-api.service';
import { TransferenciaDto } from '../../core/services/transferencias/dtos/transferencia.dto';
import { PageHeaderComponent } from '../../shared/components/page-header/page-header.component';

type LogisticaSection = 'seguimiento' | 'rutas' | 'transportistas' | 'reportes';
type CriterioRutas = 'prioridad' | 'costo' | 'tiempo';

interface TransferenciaLogisticaVm extends TransferenciaDto {
  readonly sucursal_origen_nombre: string;
  readonly sucursal_destino_nombre: string;
  readonly ruta_nombre: string;
  readonly transportista_nombre: string;
  readonly cumplimiento: 'A_TIEMPO' | 'TARDE' | 'PENDIENTE';
  readonly diferencia_horas: number | null;
}

interface CumplimientoLogisticoVm {
  readonly id_sucursal: number;
  readonly id_ruta: number;
  readonly ruta: string;
  readonly total_envios: number;
  readonly entregas_completas: number;
  readonly entregas_parciales: number;
  readonly entregas_a_tiempo: number;
  readonly entregas_tarde: number;
  readonly envios_en_curso: number;
  readonly porcentaje_cumplimiento: number;
}

@Component({
  selector: 'app-logistica-page',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, PageHeaderComponent],
  templateUrl: './logistica.page.html',
  styleUrl: './logistica.page.css',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class LogisticaPage implements OnInit {
  private readonly fb = inject(FormBuilder);
  private readonly destroyRef = inject(DestroyRef);
  private readonly logisticaApi = inject(LogisticaApiService);
  private readonly transferenciasApi = inject(TransferenciasApiService);
  private readonly sucursalesApi = inject(SucursalesApiService);

  readonly activeSection = signal<LogisticaSection>('seguimiento');
  readonly loading = signal(false);
  readonly submittingRuta = signal(false);
  readonly submittingTransportista = signal(false);
  readonly loadingReporte = signal(false);
  readonly errorMessage = signal('');
  readonly successMessage = signal('');
  readonly selectedTransferenciaId = signal<number | null>(null);
  readonly selectedRutaId = signal<number | null>(null);
  readonly selectedTransportistaId = signal<number | null>(null);
  readonly criterioRutas = signal<CriterioRutas>('prioridad');

  readonly transferencias = signal<TransferenciaDto[]>([]);
  readonly rutas = signal<RutaLogisticaDto[]>([]);
  readonly transportistas = signal<TransportistaDto[]>([]);
  readonly prioridades = signal<PrioridadRutaLogisticaDto[]>([]);
  readonly sucursales = signal<SucursalDto[]>([]);
  readonly reporteCumplimiento = signal<CumplimientoLogisticoVm[]>([]);

  readonly rutasClasificadas = signal<RutaLogisticaDto[]>([]);

  readonly rutasActivas = computed(() => this.rutas());
  readonly transportistasActivos = computed(() =>
    this.transportistas().filter((item) => item.activo)
  );

  readonly transferenciasVm = computed<TransferenciaLogisticaVm[]>(() =>
    this.transferencias().map((item) => {
      const fechaEstimada = item.envio?.fecha_estimada_llegada
        ? new Date(item.envio.fecha_estimada_llegada)
        : null;
      const fechaReal = item.envio?.fecha_real_llegada ? new Date(item.envio.fecha_real_llegada) : null;
      const diferenciaHoras =
        fechaEstimada && fechaReal
          ? Number(((fechaReal.getTime() - fechaEstimada.getTime()) / 36e5).toFixed(2))
          : null;

      return {
        ...item,
        sucursal_origen_nombre: this.getSucursalNombre(item.id_sucursal_origen),
        sucursal_destino_nombre: this.getSucursalNombre(item.id_sucursal_destino),
        ruta_nombre: this.getRutaNombre(item.envio?.id_ruta),
        transportista_nombre: this.getTransportistaNombre(item.envio?.id_transportista),
        cumplimiento:
          diferenciaHoras === null ? 'PENDIENTE' : diferenciaHoras <= 0 ? 'A_TIEMPO' : 'TARDE',
        diferencia_horas: diferenciaHoras
      };
    })
  );

  readonly filteredSeguimiento = computed(() => {
    const estado = this.seguimientoForm.controls.estado_envio.value;
    const idRuta = Number(this.seguimientoForm.controls.id_ruta.value || 0);
    const idSucursal = Number(this.seguimientoForm.controls.id_sucursal.value || 0);

    return this.transferenciasVm().filter((item) => {
      if (estado && item.envio?.estado_envio !== estado) {
        return false;
      }

      if (idRuta && item.envio?.id_ruta !== idRuta) {
        return false;
      }

      if (
        idSucursal &&
        item.id_sucursal_origen !== idSucursal &&
        item.id_sucursal_destino !== idSucursal
      ) {
        return false;
      }

      return Boolean(item.envio || item.estado === 'APROBADA' || item.estado === 'ENVIADA' || item.estado?.startsWith('RECIBIDA'));
    });
  });

  readonly selectedTransferencia = computed(() => {
    const id = this.selectedTransferenciaId();
    if (!id) {
      return null;
    }

    return this.transferenciasVm().find((item) => item.id_transferencia === id) ?? null;
  });

  readonly totalEnvios = computed(() => this.transferenciasVm().filter((item) => item.envio).length);
  readonly enviosEnCurso = computed(
    () =>
      this.transferenciasVm().filter(
        (item) => item.envio && !item.envio.fecha_real_llegada && item.envio.estado_envio === 'EN_TRANSITO'
      ).length
  );
  readonly entregasATiempo = computed(
    () => this.transferenciasVm().filter((item) => item.cumplimiento === 'A_TIEMPO').length
  );
  readonly entregasTarde = computed(
    () => this.transferenciasVm().filter((item) => item.cumplimiento === 'TARDE').length
  );

  readonly seguimientoForm = this.fb.nonNullable.group({
    estado_envio: [''],
    id_ruta: [0],
    id_sucursal: [0]
  });

  readonly rutaForm = this.fb.nonNullable.group({
    nombre_ruta: ['', [Validators.required, Validators.maxLength(120)]],
    id_prioridad_ruta: [0, [Validators.required, Validators.min(1)]],
    costo_estimado: [0, [Validators.required, Validators.min(0)]],
    tiempo_estimado: ['']
  });

  readonly transportistaForm = this.fb.nonNullable.group({
    identificacion: ['', [Validators.required, Validators.maxLength(40)]],
    nombre: ['', [Validators.required, Validators.maxLength(150)]],
    telefono: ['']
  });

  readonly reporteForm = this.fb.nonNullable.group({
    id_sucursal: [0],
    id_ruta: [0]
  });

  ngOnInit(): void {
    this.cargarVista();
  }

  seleccionarSeccion(section: LogisticaSection): void {
    this.activeSection.set(section);
    this.errorMessage.set('');
    this.successMessage.set('');
  }

  cargarVista(): void {
    this.loading.set(true);
    this.errorMessage.set('');

    forkJoin({
      transferenciasResponse: this.transferenciasApi.transferencia.listarTransferencias(),
      rutasResponse: this.logisticaApi.rutasLogistica.listarRutasLogistica(),
      prioridadesResponse: this.logisticaApi.prioridadesRutaLogistica.listarPrioridadesRutaLogistica(),
      transportistasResponse: this.logisticaApi.transportistas.listarTransportistas(),
      sucursalesResponse: this.sucursalesApi.listarSucursales(),
      reporteResponse: this.logisticaApi.rutasLogistica.reporteCumplimientoLogistico()
    })
      .pipe(
        finalize(() => this.loading.set(false)),
        takeUntilDestroyed(this.destroyRef)
      )
      .subscribe({
        next: ({
          transferenciasResponse,
          rutasResponse,
          prioridadesResponse,
          transportistasResponse,
          sucursalesResponse,
          reporteResponse
        }) => {
          const transferencias = this.extractData<TransferenciaDto[]>(transferenciasResponse);
          const rutas = this.extractData<RutaLogisticaDto[]>(rutasResponse);
          this.transferencias.set(transferencias);
          this.rutas.set(rutas);
          this.rutasClasificadas.set(rutas);
          this.prioridades.set(this.extractData<PrioridadRutaLogisticaDto[]>(prioridadesResponse));
          this.transportistas.set(this.extractData<TransportistaDto[]>(transportistasResponse));
          this.sucursales.set(this.extractData<SucursalDto[]>(sucursalesResponse));
          this.reporteCumplimiento.set(
            this.extractData<CumplimientoLogisticoVm[]>(reporteResponse)
          );
          this.ensureDefaults();

          const first = transferencias.find((item) => item.envio || item.estado === 'APROBADA' || item.estado === 'ENVIADA');
          if (first) {
            this.selectedTransferenciaId.set(first.id_transferencia);
          }
        },
        error: (error: HttpErrorResponse) => {
          this.errorMessage.set(
            this.resolveApiError(error, 'No se pudo cargar el modulo de logistica.')
          );
        }
      });
  }

  seleccionarTransferencia(idTransferencia: number): void {
    this.selectedTransferenciaId.set(idTransferencia);
  }

  clasificarRutas(criterio: CriterioRutas): void {
    this.criterioRutas.set(criterio);
    this.logisticaApi.rutasLogistica
      .clasificarRutasLogistica(criterio)
      .pipe(takeUntilDestroyed(this.destroyRef))
      .subscribe({
        next: (response) => {
          this.rutasClasificadas.set(this.extractData<RutaLogisticaDto[]>(response));
        },
        error: (error: HttpErrorResponse) => {
          this.errorMessage.set(
            this.resolveApiError(error, 'No se pudo clasificar las rutas logisticas.')
          );
        }
      });
  }

  editarRuta(ruta: RutaLogisticaDto): void {
    this.activeSection.set('rutas');
    this.selectedRutaId.set(ruta.id_ruta);
    this.rutaForm.setValue({
      nombre_ruta: ruta.nombre_ruta,
      id_prioridad_ruta: ruta.id_prioridad_ruta,
      costo_estimado: ruta.costo_estimado,
      tiempo_estimado: ruta.tiempo_estimado ?? ''
    });
  }

  guardarRuta(): void {
    if (this.rutaForm.invalid) {
      this.rutaForm.markAllAsTouched();
      return;
    }

    this.submittingRuta.set(true);
    this.errorMessage.set('');
    this.successMessage.set('');

    const value = this.rutaForm.getRawValue();
    const payload: GuardarRutaLogisticaDto = {
      nombre_ruta: value.nombre_ruta.trim(),
      id_prioridad_ruta: Number(value.id_prioridad_ruta),
      costo_estimado: Number(value.costo_estimado),
      tiempo_estimado: value.tiempo_estimado.trim() || null
    };

    const request = this.selectedRutaId()
      ? this.logisticaApi.rutasLogistica.actualizarRutaLogistica(this.selectedRutaId()!, payload)
      : this.logisticaApi.rutasLogistica.crearRutaLogistica(payload);

    request
      .pipe(
        finalize(() => this.submittingRuta.set(false)),
        takeUntilDestroyed(this.destroyRef)
      )
      .subscribe({
        next: () => {
          this.successMessage.set(
            this.selectedRutaId()
              ? 'Ruta logistica actualizada correctamente.'
              : 'Ruta logistica creada correctamente.'
          );
          this.resetRutaForm();
          this.cargarVista();
          this.activeSection.set('rutas');
        },
        error: (error: HttpErrorResponse) => {
          this.errorMessage.set(
            this.resolveApiError(error, 'No se pudo guardar la ruta logistica.')
          );
        }
      });
  }

  editarTransportista(transportista: TransportistaDto): void {
    this.activeSection.set('transportistas');
    this.selectedTransportistaId.set(transportista.id_transportista);
    this.transportistaForm.setValue({
      identificacion: transportista.identificacion,
      nombre: transportista.nombre,
      telefono: transportista.telefono ?? ''
    });
  }

  guardarTransportista(): void {
    if (this.transportistaForm.invalid) {
      this.transportistaForm.markAllAsTouched();
      return;
    }

    this.submittingTransportista.set(true);
    this.errorMessage.set('');
    this.successMessage.set('');

    const value = this.transportistaForm.getRawValue();
    const actual =
      this.transportistas().find((item) => item.id_transportista === this.selectedTransportistaId()) ??
      null;
    const payload: GuardarTransportistaDto = {
      identificacion: value.identificacion.trim(),
      nombre: value.nombre.trim(),
      telefono: value.telefono.trim() || null,
      activo: actual?.activo ?? true
    };

    const request = this.selectedTransportistaId()
      ? this.logisticaApi.transportistas.actualizarTransportista(this.selectedTransportistaId()!, payload)
      : this.logisticaApi.transportistas.crearTransportista(payload);

    request
      .pipe(
        finalize(() => this.submittingTransportista.set(false)),
        takeUntilDestroyed(this.destroyRef)
      )
      .subscribe({
        next: () => {
          this.successMessage.set(
            this.selectedTransportistaId()
              ? 'Transportista actualizado correctamente.'
              : 'Transportista creado correctamente.'
          );
          this.resetTransportistaForm();
          this.cargarVista();
          this.activeSection.set('transportistas');
        },
        error: (error: HttpErrorResponse) => {
          this.errorMessage.set(
            this.resolveApiError(error, 'No se pudo guardar el transportista.')
          );
        }
      });
  }

  toggleEstadoTransportista(transportista: TransportistaDto): void {
    const payload: GuardarTransportistaDto = {
      identificacion: transportista.identificacion,
      nombre: transportista.nombre,
      telefono: transportista.telefono,
      activo: !transportista.activo
    };

    this.logisticaApi.transportistas
      .actualizarTransportista(transportista.id_transportista, payload)
      .pipe(takeUntilDestroyed(this.destroyRef))
      .subscribe({
        next: () => {
          this.successMessage.set(
            transportista.activo
              ? 'Transportista desactivado correctamente.'
              : 'Transportista activado correctamente.'
          );
          if (this.selectedTransportistaId() === transportista.id_transportista) {
            this.resetTransportistaForm();
          }
          this.cargarVista();
        },
        error: (error: HttpErrorResponse) => {
          this.errorMessage.set(
            this.resolveApiError(error, 'No se pudo actualizar el transportista.')
          );
        }
      });
  }

  cargarReporte(): void {
    this.loadingReporte.set(true);
    this.errorMessage.set('');

    const value = this.reporteForm.getRawValue();
    this.logisticaApi.rutasLogistica
      .reporteCumplimientoLogistico(
        Number(value.id_sucursal || 0) || undefined,
        Number(value.id_ruta || 0) || undefined
      )
      .pipe(
        finalize(() => this.loadingReporte.set(false)),
        takeUntilDestroyed(this.destroyRef)
      )
      .subscribe({
        next: (response) => {
          this.reporteCumplimiento.set(this.extractData<CumplimientoLogisticoVm[]>(response));
        },
        error: (error: HttpErrorResponse) => {
          this.errorMessage.set(
            this.resolveApiError(error, 'No se pudo consultar el reporte logistico.')
          );
        }
      });
  }

  resetRutaForm(): void {
    this.selectedRutaId.set(null);
    this.rutaForm.reset({
      nombre_ruta: '',
      id_prioridad_ruta: this.prioridades()[0]?.id_prioridad_ruta ?? 0,
      costo_estimado: 0,
      tiempo_estimado: ''
    });
  }

  resetTransportistaForm(): void {
    this.selectedTransportistaId.set(null);
    this.transportistaForm.reset({
      identificacion: '',
      nombre: '',
      telefono: ''
    });
  }

  protected getSucursalNombre(idSucursal: number | null | undefined): string {
    if (!idSucursal) {
      return 'Sin sucursal';
    }

    return (
      this.sucursales().find((item) => item.id_sucursal === idSucursal)?.nombre ??
      `Sucursal #${idSucursal}`
    );
  }

  protected getRutaNombre(idRuta: number | null | undefined): string {
    if (!idRuta) {
      return 'Sin ruta';
    }

    return (
      this.rutas().find((item) => item.id_ruta === idRuta)?.nombre_ruta ?? `Ruta #${idRuta}`
    );
  }

  protected getTransportistaNombre(idTransportista: number | null | undefined): string {
    if (!idTransportista) {
      return 'Sin transportista';
    }

    return (
      this.transportistas().find((item) => item.id_transportista === idTransportista)?.nombre ??
      `Transportista #${idTransportista}`
    );
  }

  protected getCumplimientoLabel(item: TransferenciaLogisticaVm): string {
    if (!item.envio) {
      return 'Pendiente de despacho';
    }
    if (item.cumplimiento === 'PENDIENTE') {
      return 'Pendiente de entrega';
    }
    return item.cumplimiento === 'A_TIEMPO' ? 'A tiempo' : 'Con retraso';
  }

  private ensureDefaults(): void {
    if (!this.rutaForm.controls.id_prioridad_ruta.value && this.prioridades().length) {
      this.rutaForm.controls.id_prioridad_ruta.setValue(this.prioridades()[0].id_prioridad_ruta);
    }
  }

  private resolveApiError(error: HttpErrorResponse, fallback: string): string {
    const apiError = error.error as { message?: string; errors?: Record<string, string> } | null;
    const detailErrors = apiError?.errors ? Object.values(apiError.errors).join(' ') : '';

    return [detailErrors, apiError?.message, fallback].find(
      (item) => typeof item === 'string' && item.trim() !== ''
    ) as string;
  }

  private extractData<T>(response: unknown): T {
    if (this.isRecord(response)) {
      if ('data' in response) {
        return response['data'] as T;
      }
      if ('payload' in response) {
        return response['payload'] as T;
      }
      if ('result' in response) {
        return response['result'] as T;
      }
      if ('results' in response) {
        return response['results'] as T;
      }
    }

    return response as T;
  }

  private isRecord(value: unknown): value is Record<string, unknown> {
    return typeof value === 'object' && value !== null;
  }
}
