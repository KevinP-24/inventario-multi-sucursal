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
import { catchError, finalize, forkJoin, map, of, switchMap } from 'rxjs';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { faPenToSquare, faToggleOff, faToggleOn } from '@fortawesome/free-solid-svg-icons';

import { ComprasApiService } from '../../core/services/compras/compras-api.service';
import { AuthSessionService } from '../../core/services/auth/auth-session.service';
import {
  CrearDetalleOrdenCompraDto,
  DetalleOrdenCompraDto
} from '../../core/services/compras/dtos/detalle-orden-compra.dto';
import {
  EstadoOrdenCompraDto,
  HistorialComprasFiltrosDto,
  OrdenCompraDto
} from '../../core/services/compras/dtos/orden-compra.dto';
import {
  GuardarProveedorDto,
  ProveedorDto
} from '../../core/services/compras/dtos/proveedor.dto';
import { InventarioApiService } from '../../core/services/inventario/inventario-api.service';
import { ProductoDto } from '../../core/services/inventario/dtos/producto.dto';
import { ProductoUnidadDto } from '../../core/services/inventario/dtos/producto-unidad.dto';
import { SucursalDto } from '../../core/services/sucursales/dtos/sucursal.dto';
import { SucursalesApiService } from '../../core/services/sucursales/sucursales-api.service';
import { UiAlertService } from '../../core/services/ui-alert.service';
import { TipoDocumentoDto } from '../../core/services/ventas/dtos/tipo-documento.dto';
import { TiposDocumentoApiService } from '../../core/services/ventas/tipos-documento-api.service';
import { PageHeaderComponent } from '../../shared/components/page-header/page-header.component';

type ComprasSection = 'ordenes' | 'proveedores' | 'historial';

interface OrdenCompraVm extends OrdenCompraDto {
  readonly proveedor_nombre: string;
  readonly total_items: number;
  readonly puede_recibir: boolean;
  readonly puede_anular: boolean;
}

interface DetalleOrdenVm extends DetalleOrdenCompraDto {
  readonly producto: string;
  readonly codigo_producto: string;
  readonly unidad: string;
}

@Component({
  selector: 'app-compras-page',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, PageHeaderComponent, FontAwesomeModule],
  templateUrl: './compras.page.html',
  styleUrl: './compras.page.css',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class ComprasPage implements OnInit {
  private readonly fb = inject(FormBuilder);
  private readonly destroyRef = inject(DestroyRef);
  private readonly comprasApi = inject(ComprasApiService);
  private readonly authSession = inject(AuthSessionService);
  private readonly inventarioApi = inject(InventarioApiService);
  private readonly sucursalesApi = inject(SucursalesApiService);
  private readonly tiposDocumentoApi = inject(TiposDocumentoApiService);
  private readonly uiAlerts = inject(UiAlertService);
  protected readonly faPenToSquare = faPenToSquare;
  protected readonly faToggleOn = faToggleOn;
  protected readonly faToggleOff = faToggleOff;

  readonly activeSection = signal<ComprasSection>('ordenes');
  readonly loading = signal(false);
  readonly loadingDetalles = signal(false);
  readonly submittingOrden = signal(false);
  readonly submittingProveedor = signal(false);
  readonly receivingOrden = signal(false);
  readonly sugiriendoPrecio = signal(false);
  readonly ultimoPrecioSugerido = signal<number | null>(null);
  readonly errorMessage = signal('');
  readonly successMessage = signal('');

  readonly proveedores = signal<ProveedorDto[]>([]);
  readonly tiposDocumento = signal<TipoDocumentoDto[]>([]);
  readonly ordenes = signal<OrdenCompraDto[]>([]);
  readonly historial = signal<OrdenCompraDto[]>([]);
  readonly sucursales = signal<SucursalDto[]>([]);
  readonly productos = signal<ProductoDto[]>([]);
  readonly productoUnidades = signal<ProductoUnidadDto[]>([]);
  readonly draftDetalles = signal<CrearDetalleOrdenCompraDto[]>([]);
  readonly detallesOrdenSeleccionada = signal<DetalleOrdenVm[]>([]);
  readonly selectedOrdenId = signal<number | null>(null);
  readonly selectedProveedorId = signal<number | null>(null);

  readonly currentUser = this.authSession.currentUser;
  readonly usuarioId = signal<number | null>(this.resolveUsuarioId());
  readonly usuarioNombre = signal(this.resolveUsuarioNombre());
  readonly sucursalId = signal<number | null>(this.resolveSucursalOperadorId());
  readonly hasFixedSucursal = computed(() => this.sucursalId() !== null);

  readonly proveedoresActivos = computed(() => this.proveedores().filter(item => item.activo));
  readonly tiposDocumentoActivos = computed(() => this.tiposDocumento().filter(item => item.activo));
  readonly sucursalesActivas = computed(() =>
    this.sucursales().filter(item => item.estado?.toLowerCase?.() !== 'inactiva')
  );
  readonly productosActivos = computed(() => this.productos().filter(item => item.activo));
  readonly productoUnidadesActivas = computed(() =>
    this.productoUnidades().filter(item => item.activo)
  );

  readonly productosDisponiblesDetalle = computed(() => {
    const productosConUnidad = new Set(
      this.productoUnidadesActivas().map(item => Number(item.id_producto))
    );

    return this.productosActivos().filter(item =>
      productosConUnidad.has(Number(item.id_producto))
    );
  });

  protected unidadesDisponiblesDetalle(): Array<{
    id_producto_unidad: number;
    label: string;
  }> {
    const idProducto = Number(this.detalleForm.controls.id_producto.value || 0);

    if (!idProducto) {
      return [];
    }

    return this.productoUnidadesActivas()
      .filter(item => Number(item.id_producto) === idProducto)
      .sort((a, b) => {
        if (a.es_base === b.es_base) {
          return Number(a.id_producto_unidad) - Number(b.id_producto_unidad);
        }

        return a.es_base ? -1 : 1;
      })
      .map(item => ({
        id_producto_unidad: Number(item.id_producto_unidad),
        label: `${item.unidad_medida?.nombre ?? 'Unidad'} (${item.unidad_medida?.simbolo ?? '-'})`
      }));
  }

  readonly ordenesVm = computed<OrdenCompraVm[]>(() => {
    const proveedoresMap = new Map(this.proveedores().map(item => [item.id_proveedor, item]));

    return this.ordenes().map(item => ({
      ...item,
      proveedor_nombre:
        proveedoresMap.get(item.id_proveedor)?.nombre ?? `Proveedor #${item.id_proveedor}`,
      total_items: item.detalles?.length ?? 0,
      puede_recibir: item.estado === 'CREADA',
      puede_anular: item.estado === 'CREADA'
    }));
  });

  readonly historialVm = computed<OrdenCompraVm[]>(() => {
    const proveedoresMap = new Map(this.proveedores().map(item => [item.id_proveedor, item]));

    return this.historial().map(item => ({
      ...item,
      proveedor_nombre:
        proveedoresMap.get(item.id_proveedor)?.nombre ?? `Proveedor #${item.id_proveedor}`,
      total_items: item.detalles?.length ?? 0,
      puede_recibir: item.estado === 'CREADA',
      puede_anular: item.estado === 'CREADA'
    }));
  });

  readonly selectedOrden = computed(() => {
    const idOrden = this.selectedOrdenId();
    if (!idOrden) {
      return null;
    }

    return (
      this.ordenesVm().find(item => item.id_orden_compra === idOrden) ??
      this.historialVm().find(item => item.id_orden_compra === idOrden) ??
      null
    );
  });

  readonly totalOrdenes = computed(() => this.ordenesVm().length);
  readonly ordenesPendientes = computed(
    () => this.ordenesVm().filter(item => item.estado === 'CREADA').length
  );
  readonly totalProveedores = computed(() => this.proveedoresActivos().length);
  readonly draftSubtotal = computed(() =>
    this.draftDetalles().reduce((acc, item) => acc + item.cantidad * item.precio_unitario, 0)
  );
  readonly draftDescuentoTotal = computed(() =>
    this.draftDetalles().reduce((acc, item) => acc + (item.descuento ?? 0), 0)
  );
  readonly draftTotal = computed(() => this.draftSubtotal() - this.draftDescuentoTotal());

  readonly ordenForm = this.fb.nonNullable.group({
    id_proveedor: [0, [Validators.required, Validators.min(1)]],
    id_sucursal: [this.resolveSucursalOperadorId() ?? 0, [Validators.required, Validators.min(1)]],
    id_usuario: [this.resolveUsuarioId() ?? 0, [Validators.required, Validators.min(1)]],
    plazo_pago: ['']
  });

  readonly detalleForm = this.fb.nonNullable.group({
    id_producto: [0, [Validators.required, Validators.min(1)]],
    id_producto_unidad: [0, [Validators.required, Validators.min(1)]],
    cantidad: [1, [Validators.required, Validators.min(0.01)]],
    precio_unitario: [0, [Validators.required, Validators.min(0.01)]],
    descuento: [0, [Validators.min(0)]]
  });

  readonly proveedorForm = this.fb.nonNullable.group({
    id_tipo_documento: [0, [Validators.required, Validators.min(1)]],
    numero_documento: ['', [Validators.required, Validators.maxLength(40)]],
    nombre: ['', [Validators.required, Validators.maxLength(120)]],
    correo: [''],
    telefono: [''],
    direccion: ['']
  });

  readonly historialForm = this.fb.nonNullable.group({
    id_proveedor: [0],
    id_producto: [0],
    id_sucursal: [this.resolveSucursalOperadorId() ?? 0],
    estado: [''],
    fecha_desde: [''],
    fecha_hasta: ['']
  });

  ngOnInit(): void {
    this.cargarVista();

    this.detalleForm.controls.id_producto.valueChanges
      .pipe(takeUntilDestroyed(this.destroyRef))
      .subscribe(idProducto => {
        const productoId = Number(idProducto || 0);

        const unidades = this.productoUnidadesActivas().filter(
          item => Number(item.id_producto) === productoId
        );

        this.detalleForm.controls.id_producto_unidad.setValue(
          Number(unidades[0]?.id_producto_unidad ?? 0),
          { emitEvent: false }
        );

        this.detalleForm.controls.precio_unitario.setValue(0, { emitEvent: false });
        this.detalleForm.controls.precio_unitario.markAsPristine();
        this.ultimoPrecioSugerido.set(null);

        this.sugerirUltimoPrecioCompra();
      });

    this.detalleForm.controls.id_producto_unidad.valueChanges
      .pipe(takeUntilDestroyed(this.destroyRef))
      .subscribe(() => {
        this.detalleForm.controls.precio_unitario.setValue(0, { emitEvent: false });
        this.detalleForm.controls.precio_unitario.markAsPristine();
        this.ultimoPrecioSugerido.set(null);

        this.sugerirUltimoPrecioCompra();
      });

    this.ordenForm.controls.id_proveedor.valueChanges
      .pipe(takeUntilDestroyed(this.destroyRef))
      .subscribe(() => {
        this.detalleForm.controls.precio_unitario.setValue(0, { emitEvent: false });
        this.detalleForm.controls.precio_unitario.markAsPristine();
        this.ultimoPrecioSugerido.set(null);

        this.sugerirUltimoPrecioCompra();
      });
  }

  seleccionarSeccion(section: ComprasSection): void {
    this.activeSection.set(section);
    this.errorMessage.set('');
    this.successMessage.set('');
  }

  cargarVista(): void {
    this.loading.set(true);
    this.errorMessage.set('');

    forkJoin({
      proveedoresResponse: this.comprasApi.proveedores.listarProveedores(),
      tiposDocumentoResponse: this.tiposDocumentoApi.listarTiposDocumento(),
      ordenesResponse: this.comprasApi.ordenesCompra.listarOrdenesCompra(),
      sucursalesResponse: this.sucursalesApi.listarSucursales(),
      productosResponse: this.inventarioApi.productos.listarProductos(),
      productoUnidadesResponse: this.inventarioApi.productoUnidades.listarProductoUnidades()
    })
      .pipe(
        finalize(() => this.loading.set(false)),
        takeUntilDestroyed(this.destroyRef)
      )
      .subscribe({
        next: ({
          proveedoresResponse,
          tiposDocumentoResponse,
          ordenesResponse,
          sucursalesResponse,
          productosResponse,
          productoUnidadesResponse
        }) => {
          this.proveedores.set(this.extractData<ProveedorDto[]>(proveedoresResponse));
          this.tiposDocumento.set(this.extractData<TipoDocumentoDto[]>(tiposDocumentoResponse));
          const ordenes = this.extractData<OrdenCompraDto[]>(ordenesResponse);
          this.ordenes.set(ordenes);
          this.historial.set(ordenes);
          this.sucursales.set(this.extractData<SucursalDto[]>(sucursalesResponse));
          this.productos.set(this.extractData<ProductoDto[]>(productosResponse));
          this.productoUnidades.set(
            this.extractData<ProductoUnidadDto[]>(productoUnidadesResponse)
          );
          this.ensureDefaults();

          const firstOrden = ordenes[0];
          if (firstOrden) {
            this.seleccionarOrden(firstOrden.id_orden_compra);
          } else {
            this.selectedOrdenId.set(null);
            this.detallesOrdenSeleccionada.set([]);
          }
        },
        error: () => {
          this.errorMessage.set('No se pudo cargar el modulo de compras.');
          this.proveedores.set([]);
          this.tiposDocumento.set([]);
          this.ordenes.set([]);
          this.historial.set([]);
          this.sucursales.set([]);
          this.productos.set([]);
          this.productoUnidades.set([]);
          this.selectedOrdenId.set(null);
          this.detallesOrdenSeleccionada.set([]);
        }
      });
  }

  seleccionarOrden(idOrdenCompra: number): void {
    this.selectedOrdenId.set(idOrdenCompra);
    this.cargarDetallesOrden(idOrdenCompra);
  }

  cargarDetallesOrden(idOrdenCompra: number): void {
    this.loadingDetalles.set(true);

    this.comprasApi.detallesOrdenCompra
      .listarDetallesPorOrdenCompra(idOrdenCompra)
      .pipe(
        finalize(() => this.loadingDetalles.set(false)),
        takeUntilDestroyed(this.destroyRef)
      )
      .subscribe({
        next: response => {
          const detalles = this.extractData<DetalleOrdenCompraDto[]>(response);
          this.detallesOrdenSeleccionada.set(this.mapDetalles(detalles));
        },
        error: () => {
          this.detallesOrdenSeleccionada.set([]);
        }
      });
  }

  agregarDetalleOrden(): void {
    if (this.detalleForm.invalid) {
      this.detalleForm.markAllAsTouched();
      return;
    }

    const value = this.detalleForm.getRawValue();

    if (!Number(value.id_producto_unidad)) {
      void this.uiAlerts.warning(
        'El producto seleccionado no tiene una unidad activa disponible para compra.'
      );
      return;
    }

    const detalle: CrearDetalleOrdenCompraDto = {
      id_producto: Number(value.id_producto),
      id_producto_unidad: Number(value.id_producto_unidad),
      cantidad: Number(value.cantidad),
      precio_unitario: Number(value.precio_unitario),
      descuento: Number(value.descuento || 0)
    };

    this.draftDetalles.update(items => [...items, detalle]);
    this.resetDetalleForm();
  }

  removerDetalleOrden(index: number): void {
    this.draftDetalles.update(items => items.filter((_, itemIndex) => itemIndex !== index));
  }

  crearOrdenCompra(): void {
    if (this.ordenForm.invalid) {
      this.ordenForm.markAllAsTouched();
      return;
    }

    if (!this.draftDetalles().length) {
      this.errorMessage.set('Agrega al menos un producto a la orden de compra.');
      return;
    }

    this.submittingOrden.set(true);
    this.errorMessage.set('');
    this.successMessage.set('');

    const value = this.ordenForm.getRawValue();
    const payload = {
      id_proveedor: Number(value.id_proveedor),
      id_sucursal: Number(value.id_sucursal),
      id_usuario: Number(value.id_usuario),
      plazo_pago: value.plazo_pago.trim() || null,
      detalles: this.draftDetalles()
    };

    this.comprasApi.ordenesCompra
      .crearOrdenCompra(payload)
      .pipe(
        finalize(() => this.submittingOrden.set(false)),
        takeUntilDestroyed(this.destroyRef)
      )
      .subscribe({
        next: () => {
          this.successMessage.set('Orden de compra creada correctamente.');
          this.resetOrdenForm();
          this.cargarVista();
          this.activeSection.set('ordenes');
        },
        error: () => {
          this.errorMessage.set('No se pudo crear la orden de compra.');
        }
      });
  }

  recibirOrdenCompra(orden: OrdenCompraVm): void {
    if (!orden.puede_recibir) {
      return;
    }

    this.receivingOrden.set(true);
    this.errorMessage.set('');
    this.successMessage.set('');

    this.comprasApi.ordenesCompra
      .recibirOrdenCompra(orden.id_orden_compra, {
        id_usuario_recepcion: this.usuarioId() ?? 0
      })
      .pipe(
        finalize(() => this.receivingOrden.set(false)),
        takeUntilDestroyed(this.destroyRef)
      )
      .subscribe({
        next: () => {
          this.successMessage.set('Recepcion confirmada y stock actualizado correctamente.');
          this.cargarVista();
        },
        error: () => {
          this.errorMessage.set('No se pudo confirmar la recepcion de la orden.');
        }
      });
  }

  anularOrdenCompra(orden: OrdenCompraVm): void {
    if (!orden.puede_anular) {
      return;
    }

    this.comprasApi.ordenesCompra
      .anularOrdenCompra(orden.id_orden_compra)
      .pipe(takeUntilDestroyed(this.destroyRef))
      .subscribe({
        next: () => {
          this.successMessage.set('Orden de compra anulada correctamente.');
          this.cargarVista();
        },
        error: () => {
          this.errorMessage.set('No se pudo anular la orden de compra.');
        }
      });
  }

  editarProveedor(proveedor: ProveedorDto): void {
    this.activeSection.set('proveedores');
    this.selectedProveedorId.set(proveedor.id_proveedor);
    this.proveedorForm.setValue({
      id_tipo_documento: proveedor.id_tipo_documento,
      numero_documento: proveedor.numero_documento,
      nombre: proveedor.nombre,
      correo: proveedor.correo ?? '',
      telefono: proveedor.telefono ?? '',
      direccion: proveedor.direccion ?? ''
    });
  }

  guardarProveedor(): void {
    if (this.proveedorForm.invalid) {
      this.proveedorForm.markAllAsTouched();
      return;
    }

    this.submittingProveedor.set(true);
    this.errorMessage.set('');
    this.successMessage.set('');

    const value = this.proveedorForm.getRawValue();
    const proveedorActual =
      this.proveedores().find(item => item.id_proveedor === this.selectedProveedorId()) ?? null;

    const payload: GuardarProveedorDto = {
      id_tipo_documento: Number(value.id_tipo_documento),
      numero_documento: value.numero_documento.trim(),
      nombre: value.nombre.trim(),
      correo: value.correo.trim() || null,
      telefono: value.telefono.trim() || null,
      direccion: value.direccion.trim() || null,
      activo: proveedorActual?.activo ?? true
    };

    const request = this.selectedProveedorId()
      ? this.comprasApi.proveedores.actualizarProveedor(this.selectedProveedorId()!, payload)
      : this.comprasApi.proveedores.crearProveedor(payload);

    request
      .pipe(
        finalize(() => this.submittingProveedor.set(false)),
        takeUntilDestroyed(this.destroyRef)
      )
      .subscribe({
        next: () => {
          this.successMessage.set('');
          void this.uiAlerts.successToast(
            this.selectedProveedorId()
              ? 'Proveedor actualizado correctamente.'
              : 'Proveedor creado correctamente.'
          );
          this.resetProveedorForm();
          this.cargarVista();
          this.activeSection.set('proveedores');
        },
        error: (error: HttpErrorResponse) => {
          this.errorMessage.set('');
          void this.uiAlerts.error(
            this.resolveApiError(error, 'No se pudo guardar el proveedor.')
          );
        }
      });
  }

  async toggleEstadoProveedor(proveedor: ProveedorDto): Promise<void> {
    const nextActivo = !proveedor.activo;

    const confirmed = await this.uiAlerts.confirm({
      title: `${nextActivo ? 'Activar' : 'Desactivar'} proveedor`,
      text: `Se actualizara el estado de "${proveedor.nombre}".`,
      icon: 'warning',
      confirmButtonText: nextActivo ? 'Si, activar' : 'Si, desactivar'
    });

    if (!confirmed) {
      return;
    }

    const payload: GuardarProveedorDto = {
      id_tipo_documento: proveedor.id_tipo_documento,
      numero_documento: proveedor.numero_documento,
      nombre: proveedor.nombre,
      correo: proveedor.correo,
      telefono: proveedor.telefono,
      direccion: proveedor.direccion,
      activo: nextActivo
    };

    this.comprasApi.proveedores
      .actualizarProveedor(proveedor.id_proveedor, payload)
      .pipe(takeUntilDestroyed(this.destroyRef))
      .subscribe({
        next: () => {
          this.successMessage.set('');
          void this.uiAlerts.successToast(
            nextActivo
              ? 'Proveedor activado correctamente.'
              : 'Proveedor desactivado correctamente.'
          );
          if (this.selectedProveedorId() === proveedor.id_proveedor) {
            this.resetProveedorForm();
          }
          this.cargarVista();
          this.activeSection.set('proveedores');
        },
        error: (error: HttpErrorResponse) => {
          this.errorMessage.set('');
          void this.uiAlerts.error(
            nextActivo
              ? this.resolveApiError(error, 'No se pudo activar el proveedor.')
              : this.resolveApiError(error, 'No se pudo desactivar el proveedor.')
          );
        }
      });
  }
  aplicarFiltrosHistorial(): void {
    this.loading.set(true);
    this.errorMessage.set('');

    const value = this.historialForm.getRawValue();
    const filtros: HistorialComprasFiltrosDto = {
      id_proveedor: Number(value.id_proveedor || 0) || undefined,
      id_producto: Number(value.id_producto || 0) || undefined,
      id_sucursal: Number(value.id_sucursal || 0) || undefined,
      estado: (value.estado || undefined) as EstadoOrdenCompraDto | undefined,
      fecha_desde: value.fecha_desde || undefined,
      fecha_hasta: value.fecha_hasta || undefined
    };

    this.comprasApi.ordenesCompra
      .filtrarHistorialCompras(filtros)
      .pipe(
        finalize(() => this.loading.set(false)),
        takeUntilDestroyed(this.destroyRef)
      )
      .subscribe({
        next: response => {
          const historial = this.extractData<OrdenCompraDto[]>(response);
          this.historial.set(historial);

          const firstOrden = historial[0];
          if (firstOrden) {
            this.seleccionarOrden(firstOrden.id_orden_compra);
          } else {
            this.selectedOrdenId.set(null);
            this.detallesOrdenSeleccionada.set([]);
          }
        },
        error: () => {
          this.errorMessage.set('No se pudo consultar el historial de compras.');
          this.historial.set([]);
        }
      });
  }

  resetProveedorForm(): void {
    this.selectedProveedorId.set(null);
    this.proveedorForm.reset({
      id_tipo_documento: this.tiposDocumentoActivos()[0]?.id_tipo_documento ?? 0,
      numero_documento: '',
      nombre: '',
      correo: '',
      telefono: '',
      direccion: ''
    });
  }

  private resetOrdenForm(): void {
    this.ordenForm.reset({
      id_proveedor: this.proveedoresActivos()[0]?.id_proveedor ?? 0,
      id_sucursal: this.sucursalId() ?? 0,
      id_usuario: this.usuarioId() ?? 0,
      plazo_pago: ''
    });
    this.resetDetalleForm();
    this.draftDetalles.set([]);
  }

  private resetDetalleForm(): void {
    const firstProducto = this.productosDisponiblesDetalle()[0];
    const firstUnidad = this.productoUnidadesActivas().find(
      item => Number(item.id_producto) === Number(firstProducto?.id_producto ?? 0)
    );

    this.detalleForm.reset({
      id_producto: Number(firstProducto?.id_producto ?? 0),
      id_producto_unidad: Number(firstUnidad?.id_producto_unidad ?? 0),
      cantidad: 1,
      precio_unitario: 0,
      descuento: 0
    });

    this.detalleForm.controls.precio_unitario.markAsPristine();
    this.ultimoPrecioSugerido.set(null);
    this.sugerirUltimoPrecioCompra();
  }

  private sugerirUltimoPrecioCompra(): void {
    const idProveedor = Number(this.ordenForm.controls.id_proveedor.value || 0);
    const idProducto = Number(this.detalleForm.controls.id_producto.value || 0);
    const idProductoUnidad = Number(this.detalleForm.controls.id_producto_unidad.value || 0);

    if (!idProveedor || !idProducto || !idProductoUnidad) {
      this.ultimoPrecioSugerido.set(null);
      return;
    }

    this.sugiriendoPrecio.set(true);

    this.comprasApi.ordenesCompra
      .filtrarHistorialCompras({
        id_proveedor: idProveedor,
        id_producto: idProducto,
        estado: 'RECIBIDA'
      })
      .pipe(
        switchMap(response => {
          const historial = this.extractData<OrdenCompraDto[]>(response)
            .filter(item => item.estado === 'RECIBIDA')
            .sort((a, b) => {
              const fechaA = new Date(a.fecha_recepcion || a.fecha || '').getTime();
              const fechaB = new Date(b.fecha_recepcion || b.fecha || '').getTime();
              return fechaB - fechaA;
            });

          if (!historial.length) {
            return of(null);
          }

          const consultas = historial.slice(0, 5).map(orden =>
            this.comprasApi.detallesOrdenCompra
              .listarDetallesPorOrdenCompra(orden.id_orden_compra)
              .pipe(
                map(responseDetalles => {
                  const detalles = this.extractData<DetalleOrdenCompraDto[]>(responseDetalles);
                  const detalle = detalles.find(
                    item =>
                      Number(item.id_producto) === idProducto &&
                      Number(item.id_producto_unidad) === idProductoUnidad
                  );

                  return detalle?.precio_unitario ?? null;
                }),
                catchError(() => of(null))
              )
          );

          return forkJoin(consultas).pipe(
            map(precios => precios.find(precio => precio !== null) ?? null)
          );
        }),
        finalize(() => this.sugiriendoPrecio.set(false)),
        takeUntilDestroyed(this.destroyRef)
      )
      .subscribe({
        next: precio => {
          this.ultimoPrecioSugerido.set(precio);

          if (
            precio !== null &&
            (!this.detalleForm.controls.precio_unitario.dirty ||
              Number(this.detalleForm.controls.precio_unitario.value || 0) === 0)
          ) {
            this.detalleForm.controls.precio_unitario.setValue(Number(precio), {
              emitEvent: false
            });
          }
        },
        error: () => {
          this.ultimoPrecioSugerido.set(null);
        }
      });
  }

  private ensureDefaults(): void {
    if (!this.ordenForm.controls.id_proveedor.value && this.proveedoresActivos().length) {
      this.ordenForm.controls.id_proveedor.setValue(this.proveedoresActivos()[0].id_proveedor);
    }

    if (!this.proveedorForm.controls.id_tipo_documento.value && this.tiposDocumentoActivos().length) {
      this.proveedorForm.controls.id_tipo_documento.setValue(
        this.tiposDocumentoActivos()[0].id_tipo_documento
      );
    }

    if (!this.detalleForm.controls.id_producto.value && this.productosDisponiblesDetalle().length) {
      this.resetDetalleForm();
    }
  }

  private mapDetalles(detalles: DetalleOrdenCompraDto[]): DetalleOrdenVm[] {
    const productosMap = new Map(this.productos().map(item => [item.id_producto, item]));
    const unidadesMap = new Map(
      this.productoUnidades().map(item => [item.id_producto_unidad, item])
    );

    return detalles.map(item => {
      const producto = productosMap.get(item.id_producto) ?? null;
      const unidad = unidadesMap.get(item.id_producto_unidad) ?? null;

      return {
        ...item,
        producto: producto?.nombre ?? `Producto #${item.id_producto}`,
        codigo_producto: producto?.codigo ?? `PRD-${item.id_producto}`,
        unidad:
          unidad?.unidad_medida?.nombre ??
          unidad?.unidad_medida?.simbolo ??
          `Unidad #${item.id_producto_unidad}`
      };
    });
  }

  protected getProductoNombre(idProducto: number): string {
    return (
      this.productosActivos().find(item => item.id_producto === idProducto)?.nombre ??
      `Producto #${idProducto}`
    );
  }

  protected getUnidadNombre(idProductoUnidad: number): string {
    return (
      this.productoUnidadesActivas().find(
        item => Number(item.id_producto_unidad) === Number(idProductoUnidad)
      )?.unidad_medida?.nombre ?? `Unidad #${idProductoUnidad}`
    );
  }

  protected getSucursalNombre(idSucursal: number | null | undefined): string {
    if (!idSucursal) {
      return 'Sin sucursal';
    }

    return (
      this.sucursales().find(item => item.id_sucursal === idSucursal)?.nombre ??
      `Sucursal #${idSucursal}`
    );
  }

  private resolveApiError(error: HttpErrorResponse, fallback: string): string {
    const apiError = error.error as
      | { message?: string; errors?: Record<string, string | readonly string[]> }
      | null;

    const detailErrors = apiError?.errors
      ? Object.values(apiError.errors)
          .flatMap(item => (Array.isArray(item) ? item : [item]))
          .join(' ')
      : '';

    return [detailErrors, apiError?.message, fallback].find(
      item => typeof item === 'string' && item.trim() !== ''
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

  private resolveSucursalOperadorId(): number | null {
    const currentUser = this.currentUser();
    if (currentUser?.id_sucursal) {
      return currentUser.id_sucursal;
    }

    if (currentUser?.sucursal?.id_sucursal) {
      return currentUser.sucursal.id_sucursal;
    }

    const keys = ['multi-sucursal.auth.session', 'ms_user', 'auth_user', 'current_user'];

    for (const key of keys) {
      const raw = localStorage.getItem(key);
      if (!raw) {
        continue;
      }

      try {
        const parsed = JSON.parse(raw) as Record<string, unknown>;
        const idSucursal =
          this.readNestedNumber(parsed, ['user', 'id_sucursal']) ??
          this.readNestedNumber(parsed, ['user', 'sucursal', 'id_sucursal']) ??
          this.readNumber(parsed, 'id_sucursal') ??
          this.readNestedNumber(parsed, ['sucursal', 'id_sucursal']) ??
          this.readNestedNumber(parsed, ['sucursal', 'id']) ??
          this.readNestedNumber(parsed, ['usuario', 'id_sucursal']);

        if (idSucursal !== null) {
          return idSucursal;
        }
      } catch {
        //
      }
    }

    return null;
  }

  private resolveUsuarioId(): number | null {
    const currentUser = this.currentUser();
    if (currentUser?.id_usuario) {
      return currentUser.id_usuario;
    }

    const keys = ['multi-sucursal.auth.session', 'ms_user', 'auth_user', 'current_user'];

    for (const key of keys) {
      const raw = localStorage.getItem(key);
      if (!raw) {
        continue;
      }

      try {
        const parsed = JSON.parse(raw) as Record<string, unknown>;
        const idUsuario =
          this.readNestedNumber(parsed, ['user', 'id_usuario']) ??
          this.readNumber(parsed, 'id_usuario') ??
          this.readNestedNumber(parsed, ['usuario', 'id_usuario']) ??
          this.readNestedNumber(parsed, ['user', 'id_usuario']) ??
          this.readNumber(parsed, 'id');

        if (idUsuario !== null) {
          return idUsuario;
        }
      } catch {
        //
      }
    }

    return null;
  }

  private resolveUsuarioNombre(): string {
    const currentUser = this.currentUser();
    if (currentUser?.nombre?.trim()) {
      return currentUser.nombre.trim();
    }

    const keys = ['multi-sucursal.auth.session', 'ms_user', 'auth_user', 'current_user'];

    for (const key of keys) {
      const raw = localStorage.getItem(key);
      if (!raw) {
        continue;
      }

      try {
        const parsed = JSON.parse(raw) as Record<string, unknown>;
        const nombre =
          this.readNestedString(parsed, ['user', 'nombre']) ??
          this.buildNombreCompleto(parsed) ??
          this.readString(parsed, 'nombre') ??
          this.readNestedString(parsed, ['usuario', 'nombre']) ??
          this.readNestedString(parsed, ['user', 'nombre']) ??
          this.buildNombreCompletoFromPath(parsed, ['usuario']) ??
          this.buildNombreCompletoFromPath(parsed, ['user']);

        if (nombre) {
          return nombre;
        }
      } catch {
        //
      }
    }

    return 'Usuario autenticado';
  }

  private buildNombreCompleto(source: Record<string, unknown>): string | null {
    return this.joinNombreParts([
      this.readString(source, 'primer_nombre'),
      this.readString(source, 'segundo_nombre'),
      this.readString(source, 'primer_apellido'),
      this.readString(source, 'segundo_apellido')
    ]);
  }

  private buildNombreCompletoFromPath(
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

    if (!this.isRecord(current)) {
      return null;
    }

    return this.joinNombreParts([
      this.readString(current, 'primer_nombre'),
      this.readString(current, 'segundo_nombre'),
      this.readString(current, 'primer_apellido'),
      this.readString(current, 'segundo_apellido')
    ]);
  }

  private joinNombreParts(parts: Array<string | null>): string | null {
    const nombreCompleto = parts.filter((part): part is string => Boolean(part)).join(' ').trim();
    return nombreCompleto || null;
  }

  private readNumber(source: Record<string, unknown>, key: string): number | null {
    const value = source[key];

    if (typeof value === 'number' && Number.isFinite(value)) {
      return value;
    }

    if (typeof value === 'string' && value.trim() !== '' && !Number.isNaN(Number(value))) {
      return Number(value);
    }

    return null;
  }

  private readString(source: Record<string, unknown>, key: string): string | null {
    const value = source[key];

    if (typeof value === 'string' && value.trim() !== '') {
      return value.trim();
    }

    return null;
  }

  private readNestedNumber(
    source: Record<string, unknown>,
    path: readonly string[]
  ): number | null {
    let current: unknown = source;

    for (const key of path) {
      if (!this.isRecord(current) || !(key in current)) {
        return null;
      }

      current = current[key];
    }

    if (typeof current === 'number' && Number.isFinite(current)) {
      return current;
    }

    if (typeof current === 'string' && current.trim() !== '' && !Number.isNaN(Number(current))) {
      return Number(current);
    }

    return null;
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
