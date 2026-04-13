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
import { catchError, finalize, forkJoin, of } from 'rxjs';

import { AuthSessionService } from '../../core/services/auth/auth-session.service';
import { InventarioApiService } from '../../core/services/inventario/inventario-api.service';
import { InventarioSucursalDto } from '../../core/services/inventario/dtos/inventario-sucursal.dto';
import { ProductoDto } from '../../core/services/inventario/dtos/producto.dto';
import { ProductoUnidadDto } from '../../core/services/inventario/dtos/producto-unidad.dto';
import { RutasLogisticaApiService } from '../../core/services/logistica/rutas-logistica-api.service';
import { TransportistasApiService } from '../../core/services/logistica/transportistas-api.service';
import { RutaLogisticaDto } from '../../core/services/logistica/dtos/ruta-logistica.dto';
import { TransportistaDto } from '../../core/services/logistica/dtos/transportista.dto';
import { SucursalDto } from '../../core/services/sucursales/dtos/sucursal.dto';
import { SucursalesApiService } from '../../core/services/sucursales/sucursales-api.service';
import { TransferenciasApiService } from '../../core/services/transferencias/transferencias-api.service';
import {
  CrearDetalleTransferenciaDto,
  DetalleTransferenciaDto,
  RevisionTransferenciaDetalleDto
} from '../../core/services/transferencias/dtos/detalle-transferencia.dto';
import { EstadoTransferenciaDto } from '../../core/services/transferencias/dtos/estado-transferencia.dto';
import { IncidenciaTransferenciaDto } from '../../core/services/transferencias/dtos/incidencia-transferencia.dto';
import { ConfirmarRecepcionTransferenciaDto } from '../../core/services/transferencias/dtos/recepcion-transferencia.dto';
import {
  AccionRevisionTransferenciaDto,
  CrearTransferenciaDto,
  PrioridadTransferenciaDto,
  RegistrarEnvioTransferenciaDto,
  RevisarTransferenciaDto,
  TransferenciaDto
} from '../../core/services/transferencias/dtos/transferencia.dto';
import { PageHeaderComponent } from '../../shared/components/page-header/page-header.component';
import { UiAlertService } from '../../core/services/ui-alert.service';

type TransferenciasSection = 'solicitudes' | 'gestion' | 'historial';

interface TransferenciaVm extends TransferenciaDto {
  readonly sucursal_origen_nombre: string;
  readonly sucursal_destino_nombre: string;
  readonly total_items: number;
  readonly puede_revisar: boolean;
  readonly puede_enviar: boolean;
  readonly puede_recibir: boolean;
}

interface DetalleTransferenciaVm extends DetalleTransferenciaDto {
  readonly producto: string;
  readonly codigo_producto: string;
  readonly unidad: string;
}

interface RevisionDetalleDraft {
  readonly id_detalle_transferencia: number;
  readonly producto: string;
  readonly unidad: string;
  readonly cantidad_solicitada: number;
  readonly stock_disponible: number;
  cantidad_aprobada: number;
}

interface RecepcionDetalleDraft {
  readonly id_detalle_transferencia: number;
  readonly producto: string;
  readonly unidad: string;
  readonly cantidad_aprobada: number;
  cantidad_recibida: number;
  tratamiento: string;
  descripcion: string;
}

@Component({
  selector: 'app-transferencias-page',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, PageHeaderComponent],
  templateUrl: './transferencias.page.html',
  styleUrl: './transferencias.page.css',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class TransferenciasPage implements OnInit {
  private readonly fb = inject(FormBuilder);
  private readonly destroyRef = inject(DestroyRef);
  private readonly transferenciasApi = inject(TransferenciasApiService);
  private readonly inventarioApi = inject(InventarioApiService);
  private readonly sucursalesApi = inject(SucursalesApiService);
  private readonly rutasApi = inject(RutasLogisticaApiService);
  private readonly transportistasApi = inject(TransportistasApiService);
  private readonly authSession = inject(AuthSessionService);
  private readonly uiAlerts = inject(UiAlertService);

  readonly activeSection = signal<TransferenciasSection>('solicitudes');
  readonly loading = signal(false);
  readonly loadingDetalles = signal(false);
  readonly submittingTransferencia = signal(false);
  readonly submittingRevision = signal(false);
  readonly submittingEnvio = signal(false);
  readonly submittingRecepcion = signal(false);
  readonly errorMessage = signal('');
  readonly successMessage = signal('');
  readonly latestIncidencias = signal<IncidenciaTransferenciaDto[]>([]);

  readonly transferencias = signal<TransferenciaDto[]>([]);
  readonly historial = signal<TransferenciaDto[]>([]);
  readonly estados = signal<EstadoTransferenciaDto[]>([]);
  readonly productos = signal<ProductoDto[]>([]);
  readonly productoUnidades = signal<ProductoUnidadDto[]>([]);
  readonly sucursales = signal<SucursalDto[]>([]);
  readonly inventarios = signal<InventarioSucursalDto[]>([]);
  readonly rutas = signal<RutaLogisticaDto[]>([]);
  readonly transportistas = signal<TransportistaDto[]>([]);
  readonly draftDetalles = signal<CrearDetalleTransferenciaDto[]>([]);
  readonly detallesTransferenciaSeleccionada = signal<DetalleTransferenciaVm[]>([]);
  readonly reviewDrafts = signal<RevisionDetalleDraft[]>([]);
  readonly recepcionDrafts = signal<RecepcionDetalleDraft[]>([]);

  readonly selectedTransferenciaId = signal<number | null>(null);
  readonly currentUser = this.authSession.currentUser;
  readonly usuarioId = signal<number | null>(this.resolveUsuarioId());
  readonly usuarioNombre = signal(this.resolveUsuarioNombre());
  readonly sucursalId = signal<number | null>(this.resolveSucursalOperadorId());
  readonly sucursalNombre = signal(this.resolveSucursalOperadorNombre());
  readonly hasFixedSucursal = computed(() => this.sucursalId() !== null);
  readonly roleCode = computed(() => this.resolveRoleCode());
  readonly isAdminSucursal = computed(() => this.roleCode() === 'ADMIN_SUCURSAL');

  readonly productosActivos = computed(() => this.productos().filter((item) => item.activo));
  readonly productoUnidadesActivas = computed(() =>
    this.productoUnidades().filter((item) => item.activo)
  );
  readonly sucursalesActivas = computed(() =>
    this.sucursales().filter((item) => item.estado?.toLowerCase?.() !== 'inactiva')
  );
  readonly transportistasActivos = computed(() =>
    this.transportistas().filter((item) => item.activo)
  );

  protected sucursalesOrigenDisponibles(): Array<{
    id_sucursal: number;
    nombre: string;
  }> {
    const idDestino = Number(this.transferForm.controls.id_sucursal_destino.value || 0);

    const desdeCatalogo = this.sucursalesActivas()
      .filter((item) => Number(item.id_sucursal) !== idDestino)
      .map((item) => ({
        id_sucursal: Number(item.id_sucursal),
        nombre: item.nombre
      }));

    const idsCatalogo = new Set(desdeCatalogo.map((item) => item.id_sucursal));

    const desdeInventario = Array.from(
      new Set(
        this.inventarios()
          .map((item) => Number(item.id_sucursal))
          .filter((id) => id > 0 && id !== idDestino && !idsCatalogo.has(id))
      )
    ).map((id) => ({
      id_sucursal: id,
      nombre: this.getSucursalNombre(id)
    }));

    return [...desdeCatalogo, ...desdeInventario];
  }

  protected unidadesDisponiblesDetalle(): Array<{
    id_producto_unidad: number;
    label: string;
  }> {
    const idProducto = Number(this.detalleForm.controls.id_producto.value || 0);

    if (!idProducto) {
      return [];
    }

    return this.productoUnidadesActivas()
      .filter((item) => Number(item.id_producto) === idProducto)
      .sort((a, b) => {
        if (a.es_base === b.es_base) {
          return Number(a.id_producto_unidad) - Number(b.id_producto_unidad);
        }

        return a.es_base ? -1 : 1;
      })
      .map((item) => ({
        id_producto_unidad: Number(item.id_producto_unidad),
        label: this.buildUnidadLabel(item)
      }));
  }

  protected productosDisponiblesSolicitud(): ProductoDto[] {
    const idOrigen = Number(this.transferForm.controls.id_sucursal_origen.value || 0);

    if (!idOrigen) {
      return [];
    }

    const productosConStock = new Set(
      this.inventarios()
        .filter(
          (item) =>
            Number(item.id_sucursal) === idOrigen &&
            Number(item.cantidad_actual) > 0
        )
        .map((item) => Number(item.id_producto))
    );

    const productosConUnidad = new Set(
      this.productoUnidadesActivas().map((item) => Number(item.id_producto))
    );

    return this.productosActivos().filter(
      (item) =>
        productosConStock.has(Number(item.id_producto)) &&
        productosConUnidad.has(Number(item.id_producto))
    );
  }

  readonly transferenciasVm = computed<TransferenciaVm[]>(() =>
    this.transferencias().map((item) => ({
      ...item,
      sucursal_origen_nombre: this.getSucursalNombre(item.id_sucursal_origen),
      sucursal_destino_nombre: this.getSucursalNombre(item.id_sucursal_destino),
      total_items: item.detalles?.length ?? 0,
      puede_revisar:
        item.estado === 'SOLICITADA' &&
        (!this.hasFixedSucursal() || item.id_sucursal_origen === this.sucursalId()),
      puede_enviar:
        item.estado === 'APROBADA' &&
        (!this.hasFixedSucursal() || item.id_sucursal_origen === this.sucursalId()),
      puede_recibir:
        item.estado === 'ENVIADA' &&
        (!this.hasFixedSucursal() || item.id_sucursal_destino === this.sucursalId())
    }))
  );

  readonly selectedTransferencia = computed(() => {
    const idTransferencia = this.selectedTransferenciaId();
    if (!idTransferencia) {
      return null;
    }

    return this.transferenciasVm().find((item) => item.id_transferencia === idTransferencia) ?? null;
  });

  readonly bandejaVm = computed(() => this.historial());
  readonly totalTransferencias = computed(() => this.transferenciasVm().length);
  readonly pendientesRevision = computed(
    () => this.transferenciasVm().filter((item) => item.estado === 'SOLICITADA').length
  );
  readonly enTransito = computed(
    () => this.transferenciasVm().filter((item) => item.estado === 'ENVIADA').length
  );
  readonly recibidasParciales = computed(
    () => this.transferenciasVm().filter((item) => item.estado === 'RECIBIDA_PARCIAL').length
  );

  readonly transferForm = this.fb.nonNullable.group({
    id_sucursal_origen: [0, [Validators.required, Validators.min(1)]],
    id_sucursal_destino: [this.resolveSucursalOperadorId() ?? 0, [Validators.required, Validators.min(1)]],
    prioridad: ['NORMAL' as PrioridadTransferenciaDto, [Validators.required]],
    observacion: ['']
  });

  readonly detalleForm = this.fb.nonNullable.group({
    id_producto: [0, [Validators.required, Validators.min(1)]],
    id_producto_unidad: [0, [Validators.required, Validators.min(1)]],
    cantidad_solicitada: [1, [Validators.required, Validators.min(0.01)]]
  });

  readonly revisionForm = this.fb.nonNullable.group({
    accion: ['APROBAR' as AccionRevisionTransferenciaDto, [Validators.required]],
    observacion: ['']
  });

  readonly envioForm = this.fb.nonNullable.group({
    id_ruta: [0, [Validators.required, Validators.min(1)]],
    id_transportista: [0, [Validators.required, Validators.min(1)]],
    fecha_estimada_llegada: ['']
  });

  readonly recepcionForm = this.fb.nonNullable.group({
    observacion: ['']
  });

  readonly filtrosForm = this.fb.nonNullable.group({
    estado: [''],
    id_sucursal_origen: [0],
    id_sucursal_destino: [0],
    fecha_desde: [''],
    fecha_hasta: ['']
  });

  ngOnInit(): void {
    this.cargarVista();

    this.detalleForm.controls.id_producto.valueChanges
      .pipe(takeUntilDestroyed(this.destroyRef))
      .subscribe((idProducto) => {
        const unidades = this.productoUnidadesActivas().filter(
          (item) => Number(item.id_producto) === Number(idProducto || 0)
        );

        this.detalleForm.controls.id_producto_unidad.setValue(
          Number(unidades[0]?.id_producto_unidad ?? 0),
          { emitEvent: false }
        );
      });

    this.transferForm.controls.id_sucursal_origen.valueChanges
      .pipe(takeUntilDestroyed(this.destroyRef))
      .subscribe(() => this.sincronizarDetalleSolicitud());
  }

  seleccionarSeccion(section: TransferenciasSection): void {
    this.activeSection.set(section);
    this.errorMessage.set('');
    this.successMessage.set('');
  }

  cargarVista(): void {
    this.loading.set(true);
    this.errorMessage.set('');

    forkJoin({
      transferenciasResponse: this.transferenciasApi.transferencia.listarTransferencias(),
      estadosResponse: this.transferenciasApi.estadosTransferencia.listarEstadosTransferencia(),
      productosResponse: this.inventarioApi.productos.listarProductos(),
      productoUnidadesResponse: this.inventarioApi.productoUnidades.listarProductoUnidades(),
      sucursalesResponse: this.sucursalesApi
      .listarSucursales()
      .pipe(catchError(() => of([] as SucursalDto[]))),
      inventariosResponse: this.inventarioApi.inventarioSucursal.listarInventarioSucursal(),
      rutasResponse: this.rutasApi.listarRutasLogistica(),
      transportistasResponse: this.transportistasApi.listarTransportistas()
    })
      .pipe(
        finalize(() => this.loading.set(false)),
        takeUntilDestroyed(this.destroyRef)
      )
      .subscribe({
        next: ({
          transferenciasResponse,
          estadosResponse,
          productosResponse,
          productoUnidadesResponse,
          sucursalesResponse,
          inventariosResponse,
          rutasResponse,
          transportistasResponse
        }) => {
          const transferencias = this.extractData<TransferenciaDto[]>(transferenciasResponse);
          this.transferencias.set(transferencias);
          this.historial.set(transferencias);
          this.estados.set(this.extractData<EstadoTransferenciaDto[]>(estadosResponse));
          this.productos.set(this.extractData<ProductoDto[]>(productosResponse));
          this.productoUnidades.set(
            this.extractData<ProductoUnidadDto[]>(productoUnidadesResponse)
          );
          this.sucursales.set(this.extractData<SucursalDto[]>(sucursalesResponse));
          this.inventarios.set(this.extractData<InventarioSucursalDto[]>(inventariosResponse));
          this.rutas.set(this.extractData<RutaLogisticaDto[]>(rutasResponse));
          this.transportistas.set(this.extractData<TransportistaDto[]>(transportistasResponse));
          this.ensureDefaults();

          const firstTransfer = transferencias[0];
          if (firstTransfer) {
            this.seleccionarTransferencia(firstTransfer.id_transferencia);
          } else {
            this.selectedTransferenciaId.set(null);
            this.detallesTransferenciaSeleccionada.set([]);
            this.reviewDrafts.set([]);
            this.recepcionDrafts.set([]);
          }
        },
        error: (error: HttpErrorResponse) => {
          this.errorMessage.set(
            this.resolveApiError(error, 'No se pudo cargar el modulo de transferencias.')
          );
        }
      });
  }

  seleccionarTransferencia(idTransferencia: number): void {
    this.selectedTransferenciaId.set(idTransferencia);
    this.latestIncidencias.set([]);
    this.cargarDetallesTransferencia(idTransferencia);
  }

  cargarDetallesTransferencia(idTransferencia: number): void {
    this.loadingDetalles.set(true);

    this.transferenciasApi.detallesTransferencia
      .listarDetallesPorTransferencia(idTransferencia)
      .pipe(
        finalize(() => this.loadingDetalles.set(false)),
        takeUntilDestroyed(this.destroyRef)
      )
      .subscribe({
        next: (response) => {
          const detalles = this.mapDetalles(
            this.extractData<DetalleTransferenciaDto[]>(response)
          );
          this.detallesTransferenciaSeleccionada.set(detalles);
          this.syncReviewDrafts(detalles);
          this.syncRecepcionDrafts(detalles);
        },
        error: () => {
          this.detallesTransferenciaSeleccionada.set([]);
          this.reviewDrafts.set([]);
          this.recepcionDrafts.set([]);
        }
      });
  }

  agregarDetalleSolicitud(): void {
    if (this.detalleForm.invalid) {
      this.detalleForm.markAllAsTouched();
      this.errorMessage.set('');
      void this.uiAlerts.warning('Completa producto, unidad y cantidad para agregar el detalle.');
      return;
    }

    const value = this.detalleForm.getRawValue();
    const detalle: CrearDetalleTransferenciaDto = {
      id_producto: Number(value.id_producto),
      id_producto_unidad: Number(value.id_producto_unidad),
      cantidad_solicitada: Number(value.cantidad_solicitada)
    };

    this.draftDetalles.update((items) => [...items, detalle]);
    this.resetDetalleForm();
  }

  removerDetalleSolicitud(index: number): void {
    this.draftDetalles.update((items) => items.filter((_, itemIndex) => itemIndex !== index));
  }

  async crearTransferencia(): Promise<void> {
    if (this.transferForm.invalid) {
      this.transferForm.markAllAsTouched();
      return;
    }

    if (!this.draftDetalles().length) {
      void this.uiAlerts.warning('Agrega al menos un producto a la solicitud de transferencia.');
      return;
    }

    const confirmed = await this.uiAlerts.confirm({
      title: 'Crear solicitud',
      text: '¿Confirmas la creacion de esta solicitud de transferencia?',
      icon: 'question',
      confirmButtonText: 'Si, crear'
    });

    if (!confirmed) return;

    this.submittingTransferencia.set(true);

    const value = this.transferForm.getRawValue();
    const payload: CrearTransferenciaDto = {
      id_sucursal_origen: Number(value.id_sucursal_origen),
      id_sucursal_destino: Number(value.id_sucursal_destino),
      id_usuario_solicita: this.usuarioId() ?? 0,
      prioridad: value.prioridad,
      observacion: value.observacion.trim() || null,
      detalles: this.draftDetalles()
    };

    this.transferenciasApi.transferencia
      .crearTransferencia(payload)
      .pipe(
        finalize(() => this.submittingTransferencia.set(false)),
        takeUntilDestroyed(this.destroyRef)
      )
      .subscribe({
        next: (response) => {
          const transferencia = this.extractData<TransferenciaDto>(response);
          void this.uiAlerts.successToast(
            `Transferencia #${transferencia.id_transferencia} creada correctamente.`
          );
          this.resetTransferenciaForm();
          this.cargarVista();
        },
        error: (error: HttpErrorResponse) => {
          const errorMsg = this.resolveApiError(
            error,
            'No se pudo cargar el modulo de transferencias.'
          );
          this.errorMessage.set(errorMsg);
          void this.uiAlerts.error(errorMsg);
        }
      });
  }

  async aprobarTransferencia(): Promise<void> {
    const selected = this.selectedTransferencia();
    if (!selected) {
      return;
    }

    const confirmed = await this.uiAlerts.confirm({
      title: 'Aprobar transferencia',
      text: `¿Confirmas la aprobacion de la transferencia #${selected.id_transferencia}? Luego podras registrar el envio y descontar el inventario en origen.`,
      icon: 'warning',
      confirmButtonText: 'Si, aprobar'
    });

    if (!confirmed) return;

    const payload: RevisarTransferenciaDto = {
      accion: 'APROBAR',
      observacion: this.revisionForm.controls.observacion.value.trim() || null,
      detalles: this.reviewDrafts().map(
        (item): RevisionTransferenciaDetalleDto => ({
          id_detalle_transferencia: item.id_detalle_transferencia,
          cantidad_aprobada: Number(item.cantidad_aprobada)
        })
      )
    };

    this.submittingRevision.set(true);
    this.transferenciasApi.transferencia
      .revisarTransferencia(selected.id_transferencia, payload)
      .pipe(
        finalize(() => this.submittingRevision.set(false)),
        takeUntilDestroyed(this.destroyRef)
      )
      .subscribe({
        next: () => {
          void this.uiAlerts.successToast('Transferencia aprobada correctamente.');
          this.cargarVista();
        },
        error: (error: HttpErrorResponse) => {
          const errorMsg = this.resolveApiError(error, 'No se pudo aprobar la transferencia.');
          this.errorMessage.set(errorMsg);
          void this.uiAlerts.error(errorMsg);
        }
      });
  }

  async rechazarTransferencia(): Promise<void> {
    const selected = this.selectedTransferencia();
    if (!selected) {
      return;
    }

    const confirmed = await this.uiAlerts.confirm({
      title: 'Rechazar transferencia',
      text: `¿Confirmas el rechazo definitivo de la transferencia #${selected.id_transferencia}?`,
      icon: 'warning',
      confirmButtonText: 'Si, rechazar',
      cancelButtonText: 'Cancelar'
    });

    if (!confirmed) return;

    const payload: RevisarTransferenciaDto = {
      accion: 'RECHAZAR',
      observacion: this.revisionForm.controls.observacion.value.trim() || null
    };

    this.submittingRevision.set(true);
    this.transferenciasApi.transferencia
      .revisarTransferencia(selected.id_transferencia, payload)
      .pipe(
        finalize(() => this.submittingRevision.set(false)),
        takeUntilDestroyed(this.destroyRef)
      )
      .subscribe({
        next: () => {
          void this.uiAlerts.successToast('Transferencia rechazada correctamente.');
          this.cargarVista();
        },
        error: (error: HttpErrorResponse) => {
          const errorMsg = this.resolveApiError(error, 'No se pudo rechazar la transferencia.');
          this.errorMessage.set(errorMsg);
          void this.uiAlerts.error(errorMsg);
        }
      });
  }

  async registrarEnvio(): Promise<void> {
    const selected = this.selectedTransferencia();
    if (!selected) {
      return;
    }

    if (this.envioForm.invalid) {
      this.envioForm.markAllAsTouched();
      return;
    }

    const confirmed = await this.uiAlerts.confirm({
      title: 'Registrar envio',
      text: `¿Confirmas que la mercancia de la transferencia #${selected.id_transferencia} fue despachada?`,
      icon: 'question',
      confirmButtonText: 'Si, registrar envio'
    });

    if (!confirmed) return;

    const value = this.envioForm.getRawValue();
    const payload: RegistrarEnvioTransferenciaDto = {
      id_ruta: Number(value.id_ruta),
      id_transportista: Number(value.id_transportista),
      fecha_estimada_llegada: value.fecha_estimada_llegada || null
    };

    this.submittingEnvio.set(true);
    this.transferenciasApi.transferencia
      .registrarEnvioTransferencia(selected.id_transferencia, payload)
      .pipe(
        finalize(() => this.submittingEnvio.set(false)),
        takeUntilDestroyed(this.destroyRef)
      )
      .subscribe({
        next: () => {
          void this.uiAlerts.successToast('Envio registrado y transferencia puesta en transito.');
          this.cargarVista();
        },
        error: (error: HttpErrorResponse) => {
          const errorMsg = this.resolveApiError(error, 'No se pudo registrar el envio de la transferencia.');
          this.errorMessage.set(errorMsg);
          void this.uiAlerts.error(errorMsg);
        }
      });
  }

  async confirmarRecepcion(): Promise<void> {
    const selected = this.selectedTransferencia();
    if (!selected) {
      return;
    }

    const confirmed = await this.uiAlerts.confirm({
      title: 'Confirmar recepcion',
      text: `¿Confirmas la recepcion de la mercancia de la transferencia #${selected.id_transferencia}? Esto afectara el inventario local.`,
      icon: 'warning',
      confirmButtonText: 'Si, confirmar recepcion'
    });

    if (!confirmed) return;

    const payload: ConfirmarRecepcionTransferenciaDto = {
      id_usuario_recibe: this.usuarioId() ?? 0,
      tipo_recepcion: this.recepcionDrafts().some((item) => item.cantidad_recibida < item.cantidad_aprobada)
        ? 'PARCIAL'
        : 'COMPLETA',
      observacion: this.recepcionForm.controls.observacion.value.trim() || null,
      detalles: this.recepcionDrafts().map((item) => ({
        id_detalle_transferencia: item.id_detalle_transferencia,
        cantidad_recibida: Number(item.cantidad_recibida),
        tratamiento: item.tratamiento || undefined,
        descripcion: item.descripcion.trim() || null
      }))
    };

    this.submittingRecepcion.set(true);
    this.transferenciasApi.transferencia
      .confirmarRecepcionTransferencia(selected.id_transferencia, payload)
      .pipe(
        finalize(() => this.submittingRecepcion.set(false)),
        takeUntilDestroyed(this.destroyRef)
      )
      .subscribe({
        next: (response) => {
          const result = this.extractData<{
            transferencia: TransferenciaDto;
            recepcion: { incidencias: IncidenciaTransferenciaDto[] };
          }>(response);
          this.latestIncidencias.set(result.recepcion?.incidencias ?? []);
          
          void this.uiAlerts.success('Recepcion registrada y stock actualizado correctamente.', 'Terminado');
          this.cargarVista();
        },
        error: (error: HttpErrorResponse) => {
          const errorMsg = this.resolveApiError(error, 'No se pudo confirmar la recepcion.');
          this.errorMessage.set(errorMsg);
          void this.uiAlerts.error(errorMsg);
        }
      });
  }

  aplicarFiltros(): void {
    const value = this.filtrosForm.getRawValue();
    const historial = this.transferencias().filter((item) => {
      if (value.estado && item.estado !== value.estado) {
        return false;
      }

      if (Number(value.id_sucursal_origen || 0) && item.id_sucursal_origen !== Number(value.id_sucursal_origen)) {
        return false;
      }

      if (Number(value.id_sucursal_destino || 0) && item.id_sucursal_destino !== Number(value.id_sucursal_destino)) {
        return false;
      }

      if (value.fecha_desde && item.fecha_solicitud && item.fecha_solicitud.slice(0, 10) < value.fecha_desde) {
        return false;
      }

      if (value.fecha_hasta && item.fecha_solicitud && item.fecha_solicitud.slice(0, 10) > value.fecha_hasta) {
        return false;
      }

      return true;
    });

    this.historial.set(historial);

    const firstTransfer = historial[0];
    if (firstTransfer) {
      this.seleccionarTransferencia(firstTransfer.id_transferencia);
    } else {
      this.selectedTransferenciaId.set(null);
      this.detallesTransferenciaSeleccionada.set([]);
    }
  }

  updateRevisionCantidad(idDetalle: number, value: string): void {
    this.reviewDrafts.update((items) =>
      items.map((item) =>
        item.id_detalle_transferencia === idDetalle
          ? { ...item, cantidad_aprobada: Number(value || 0) }
          : item
      )
    );
  }

  updateRecepcionCantidad(idDetalle: number, value: string): void {
    this.recepcionDrafts.update((items) =>
      items.map((item) =>
        item.id_detalle_transferencia === idDetalle
          ? { ...item, cantidad_recibida: Number(value || 0) }
          : item
      )
    );
  }

  updateRecepcionTratamiento(idDetalle: number, value: string): void {
    this.recepcionDrafts.update((items) =>
      items.map((item) =>
        item.id_detalle_transferencia === idDetalle
          ? { ...item, tratamiento: value }
          : item
      )
    );
  }

  updateRecepcionDescripcion(idDetalle: number, value: string): void {
    this.recepcionDrafts.update((items) =>
      items.map((item) =>
        item.id_detalle_transferencia === idDetalle
          ? { ...item, descripcion: value }
          : item
      )
    );
  }

  protected getProductoNombre(idProducto: number): string {
    return (
      this.productos().find((item) => item.id_producto === idProducto)?.nombre ??
      `Producto #${idProducto}`
    );
  }

private getProductoUnidadById(idProductoUnidad: number): ProductoUnidadDto | null {
  return (
    this.productoUnidadesActivas().find(
      (item) => Number(item.id_producto_unidad) === Number(idProductoUnidad)
    ) ?? null
  );
}

private getInventarioProductoSucursal(
  idProducto: number,
  idSucursal: number
): InventarioSucursalDto | null {
  return (
    this.inventarios().find(
      (item) =>
        Number(item.id_producto) === Number(idProducto) &&
        Number(item.id_sucursal) === Number(idSucursal)
    ) ?? null
  );
}

private getStockDisponibleEnUnidad(
  idProducto: number,
  idSucursal: number,
  idProductoUnidad: number
): number {
  const inventario = this.getInventarioProductoSucursal(idProducto, idSucursal);
  const productoUnidad = this.getProductoUnidadById(idProductoUnidad);

  if (!inventario || !productoUnidad) {
    return 0;
  }

  const factor = Number(productoUnidad.factor_conversion || 1);

  if (!factor || factor <= 0) {
    return 0;
  }

  return Number(inventario.cantidad_actual) / factor;
}

private buildUnidadLabel(unidad: ProductoUnidadDto): string {
  const nombre = unidad.unidad_medida?.nombre?.trim() || 'Unidad';
  const simboloPropio = unidad.unidad_medida?.simbolo?.trim() || 'und';
  const factor = Number(unidad.factor_conversion ?? 1);

  const unidadBase = this.productoUnidadesActivas().find(
    (item) =>
      Number(item.id_producto) === Number(unidad.id_producto) &&
      Boolean(item.es_base)
  );

  const simboloBase = unidadBase?.unidad_medida?.simbolo?.trim() || simboloPropio || 'und';
  const factorTexto = this.formatFactor(factor);

  if (unidad.es_base) {
    return `${nombre} base (1 ${simboloBase})`;
  }

  return `${nombre} (${factorTexto} ${simboloBase})`;
}

  private formatFactor(value: number): string {
    const normalized = Number(value);

    if (!Number.isFinite(normalized) || normalized <= 0) {
      return '1';
    }

    return Number.isInteger(normalized)
      ? String(normalized)
      : normalized.toFixed(2).replace(/\.?0+$/, '');
  }

  protected stockDisponibleDetalle(): string {
    const idProducto = Number(this.detalleForm.controls.id_producto.value || 0);
    const idSucursal = Number(this.transferForm.controls.id_sucursal_origen.value || 0);
    const idProductoUnidad = Number(this.detalleForm.controls.id_producto_unidad.value || 0);

    if (!idProducto || !idSucursal || !idProductoUnidad) {
      return 'Sin inventario';
    }

    const disponible = this.getStockDisponibleEnUnidad(
      idProducto,
      idSucursal,
      idProductoUnidad
    );

    const unidad = this.getProductoUnidadById(idProductoUnidad);
    const simbolo = unidad?.unidad_medida?.simbolo ?? '';

    return `${disponible.toLocaleString('es-CO', {
      minimumFractionDigits: 0,
      maximumFractionDigits: 2
    })}${simbolo ? ` ${simbolo}` : ''}`;
  }

  protected getUnidadNombre(idProductoUnidad: number): string {
    const unidad = this.productoUnidadesActivas().find(
      (item) => Number(item.id_producto_unidad) === Number(idProductoUnidad)
    );

    return unidad ? this.buildUnidadLabel(unidad) : `Unidad #${idProductoUnidad}`;
  }

  protected getSucursalNombre(idSucursal: number | null | undefined): string {
    if (!idSucursal) {
      return 'Sin sucursal';
    }

    const nombreDesdeListado =
      this.sucursales().find((item) => Number(item.id_sucursal) === Number(idSucursal))?.nombre ?? null;

    if (nombreDesdeListado) {
      return nombreDesdeListado;
    }

    if (Number(this.sucursalId() || 0) === Number(idSucursal) && this.sucursalNombre()) {
      return this.sucursalNombre();
    }

    return `Sucursal #${idSucursal}`;
  }

  protected getStockOrigen(idProducto: number, idSucursal: number): number {
    return (
      this.inventarios().find(
        (item) => item.id_producto === idProducto && item.id_sucursal === idSucursal
      )?.cantidad_actual ?? 0
    );
  }

  private sincronizarDetalleSolicitud(): void {
    const productos = this.productosDisponiblesSolicitud();
    const idProductoActual = Number(this.detalleForm.controls.id_producto.value || 0);

    if (!productos.some((item) => Number(item.id_producto) === idProductoActual)) {
      this.resetDetalleForm();
      return;
    }

    const unidades = this.unidadesDisponiblesDetalle();
    const idUnidadActual = Number(this.detalleForm.controls.id_producto_unidad.value || 0);

    if (!unidades.some((item) => item.id_producto_unidad === idUnidadActual)) {
      this.detalleForm.controls.id_producto_unidad.setValue(
        unidades[0]?.id_producto_unidad ?? 0,
        { emitEvent: false }
      );
    }
  }

  protected getFaltanteRecepcion(item: RecepcionDetalleDraft): number {
    return Math.max(item.cantidad_aprobada - item.cantidad_recibida, 0);
  }

  private ensureDefaults(): void {
    if (!this.transferForm.controls.id_sucursal_destino.value && this.sucursalId()) {
      this.transferForm.controls.id_sucursal_destino.setValue(this.sucursalId()!);
    }

    if (
      !this.transferForm.controls.id_sucursal_origen.value &&
      this.sucursalesOrigenDisponibles().length
    ) {
      this.transferForm.controls.id_sucursal_origen.setValue(
        this.sucursalesOrigenDisponibles()[0].id_sucursal
      );
    }

    if (!this.detalleForm.controls.id_producto.value && this.productosDisponiblesSolicitud().length) {
      this.resetDetalleForm();
    }

    if (!this.envioForm.controls.id_ruta.value && this.rutas().length) {
      this.envioForm.controls.id_ruta.setValue(this.rutas()[0].id_ruta);
    }

    if (!this.envioForm.controls.id_transportista.value && this.transportistasActivos().length) {
      this.envioForm.controls.id_transportista.setValue(
        this.transportistasActivos()[0].id_transportista
      );
    }
  }

  private syncReviewDrafts(detalles: DetalleTransferenciaVm[]): void {
    const selected = this.selectedTransferencia();
    if (!selected) {
      this.reviewDrafts.set([]);
      return;
    }

    this.reviewDrafts.set(
      detalles.map((item) => ({
        id_detalle_transferencia: item.id_detalle_transferencia,
        producto: item.producto,
        unidad: item.unidad,
        cantidad_solicitada: item.cantidad_solicitada,
        stock_disponible: this.getStockDisponibleEnUnidad(
          item.id_producto,
          selected.id_sucursal_origen,
          item.id_producto_unidad
        ),
        cantidad_aprobada: item.cantidad_aprobada
      }))
    );
  }

  private syncRecepcionDrafts(detalles: DetalleTransferenciaVm[]): void {
    this.recepcionDrafts.set(
      detalles
        .filter((item) => item.cantidad_aprobada > 0)
        .map((item) => ({
          id_detalle_transferencia: item.id_detalle_transferencia,
          producto: item.producto,
          unidad: item.unidad,
          cantidad_aprobada: item.cantidad_aprobada,
          cantidad_recibida: item.cantidad_aprobada,
          tratamiento: '',
          descripcion: ''
        }))
    );
  }

  private resetTransferenciaForm(): void {
    this.transferForm.reset({
      id_sucursal_origen: this.sucursalesOrigenDisponibles()[0]?.id_sucursal ?? 0,
      id_sucursal_destino: this.sucursalId() ?? 0,
      prioridad: 'NORMAL',
      observacion: ''
    });
    this.draftDetalles.set([]);
    this.resetDetalleForm();
  }

  private resetDetalleForm(): void {
    const firstProducto = this.productosDisponiblesSolicitud()[0];
    const firstUnidad = this.productoUnidadesActivas().find(
      (item) => Number(item.id_producto) === Number(firstProducto?.id_producto ?? 0)
    );

    this.detalleForm.reset({
      id_producto: Number(firstProducto?.id_producto ?? 0),
      id_producto_unidad: Number(firstUnidad?.id_producto_unidad ?? 0),
      cantidad_solicitada: 1
    });
  }

  private mapDetalles(detalles: DetalleTransferenciaDto[]): DetalleTransferenciaVm[] {
    const productosMap = new Map(this.productos().map((item) => [item.id_producto, item]));
    const unidadesMap = new Map(
      this.productoUnidades().map((item) => [item.id_producto_unidad, item])
    );

    return detalles.map((item) => {
      const producto = productosMap.get(item.id_producto) ?? null;
      const unidad = unidadesMap.get(item.id_producto_unidad) ?? null;

      return {
        ...item,
        producto: producto?.nombre ?? `Producto #${item.id_producto}`,
        codigo_producto: producto?.codigo ?? `PRD-${item.id_producto}`,
        unidad: unidad ? this.buildUnidadLabel(unidad) : `Unidad #${item.id_producto_unidad}`
      };
    });
  }

  private resolveRoleCode(): string | null {
    const currentUser = this.currentUser();
    const roleCode = currentUser?.rol?.codigo?.trim?.().toUpperCase?.();
    if (roleCode) {
      return roleCode;
    }

    const roleName = currentUser?.rol?.nombre?.trim?.().toLowerCase?.();
    if (roleName === 'admin sucursal' || roleName === 'administrador de sucursal') {
      return 'ADMIN_SUCURSAL';
    }

    if (roleName === 'operario de inventario') {
      return 'OPERARIO_INVENTARIO';
    }

    return null;
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

  private resolveSucursalOperadorNombre(): string {
    const currentUser = this.currentUser();

    if (currentUser?.sucursal?.nombre?.trim()) {
      return currentUser.sucursal.nombre.trim();
    }

    const keys = ['multi-sucursal.auth.session', 'ms_user', 'auth_user', 'current_user'];

    for (const key of keys) {
      const raw = localStorage.getItem(key);
      if (!raw) {
        continue;
      }

      try {
        const parsed = JSON.parse(raw) as Record<string, unknown>;
        const nombreSucursal =
          this.readNestedString(parsed, ['user', 'sucursal', 'nombre']) ??
          this.readNestedString(parsed, ['sucursal', 'nombre']) ??
          this.readNestedString(parsed, ['usuario', 'sucursal', 'nombre']);

        if (nombreSucursal) {
          return nombreSucursal;
        }
      } catch {
        //
      }
    }

    return '';
  }

  private resolveSucursalOperadorId(): number | null {
    const currentUser = this.currentUser();
    if (currentUser?.id_sucursal) {
      return currentUser.id_sucursal;
    }
    if (currentUser?.sucursal?.id_sucursal) {
      return currentUser.sucursal.id_sucursal;
    }
    return null;
  }

  private resolveUsuarioId(): number | null {
    return this.currentUser()?.id_usuario ?? null;
  }

  private resolveUsuarioNombre(): string {
    return this.currentUser()?.nombre?.trim() || 'Usuario actual';
  }

  private readNestedString(
    source: Record<string, unknown>,
    path: readonly string[]
  ): string | null {
    let current: unknown = source;

    for (const key of path) {
      if (!this.isRecord(current) || !(key in current)) {
        return null;
      }

      current = current[key];
    }

    if (typeof current === 'string' && current.trim() !== '') {
      return current.trim();
    }

    return null;
  }
}
