import { CommonModule } from '@angular/common';
import { HttpErrorResponse } from '@angular/common/http';
import { generarComprobanteVentaPdf } from '../../core/utils/pdf-comprobante.util';
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
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import {
  faPenToSquare,
  faToggleOff,
  faToggleOn
} from '@fortawesome/free-solid-svg-icons';
import { UiAlertService } from '../../core/services/ui-alert.service';
import { AuthSessionService } from '../../core/services/auth/auth-session.service';
import { InventarioApiService } from '../../core/services/inventario/inventario-api.service';
import { InventarioSucursalDto } from '../../core/services/inventario/dtos/inventario-sucursal.dto';
import {
  GuardarListaPrecioDto,
  ListaPrecioDto
} from '../../core/services/inventario/dtos/lista-precio.dto';
import { PrecioProductoDto } from '../../core/services/inventario/dtos/precio-producto.dto';
import { ProductoDto } from '../../core/services/inventario/dtos/producto.dto';
import { ProductoUnidadDto } from '../../core/services/inventario/dtos/producto-unidad.dto';
import { SucursalDto } from '../../core/services/sucursales/dtos/sucursal.dto';
import { SucursalesApiService } from '../../core/services/sucursales/sucursales-api.service';
import {
  ClienteDto,
  GuardarClienteDto
} from '../../core/services/ventas/dtos/cliente.dto';
import {
  CrearDetalleVentaDto,
  DetalleVentaDto
} from '../../core/services/ventas/dtos/detalle-venta.dto';
import { TipoDocumentoDto } from '../../core/services/ventas/dtos/tipo-documento.dto';
import { CrearVentaDto, VentaDto } from '../../core/services/ventas/dtos/venta.dto';
import { VentasApiService } from '../../core/services/ventas/ventas-api.service';
import { PageHeaderComponent } from '../../shared/components/page-header/page-header.component';

type VentasSection = 'ventas' | 'clientes' | 'precios' | 'historial';

interface VentaVm extends VentaDto {
  readonly cliente_nombre: string;
  readonly lista_precio_nombre: string;
  readonly total_items: number;
}

interface DetalleVentaVm extends DetalleVentaDto {
  readonly producto: string;
  readonly codigo_producto: string;
  readonly unidad: string;
}

interface PrecioProductoVm extends PrecioProductoDto {
  readonly producto_nombre: string;
  readonly codigo_producto: string;
  readonly lista_nombre: string;
}

@Component({
  selector: 'app-ventas-page',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, PageHeaderComponent, FontAwesomeModule],
  templateUrl: './ventas.page.html',
  styleUrl: './ventas.page.css',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class VentasPage implements OnInit {
  private readonly fb = inject(FormBuilder);
  private readonly destroyRef = inject(DestroyRef);
  private readonly ventasApi = inject(VentasApiService);
  private readonly inventarioApi = inject(InventarioApiService);
  private readonly sucursalesApi = inject(SucursalesApiService);
  private readonly uiAlerts = inject(UiAlertService);

  protected readonly faPenToSquare = faPenToSquare;
  protected readonly faToggleOn = faToggleOn;
  protected readonly faToggleOff = faToggleOff;
  private readonly authSession = inject(AuthSessionService);
  readonly activeSection = signal<VentasSection>('ventas');
  readonly loading = signal(false);
  readonly loadingDetalles = signal(false);
  readonly submittingVenta = signal(false);
  readonly submittingCliente = signal(false);
  readonly submittingLista = signal(false);
  readonly submittingPrecio = signal(false);
  readonly errorMessage = signal('');
  readonly successMessage = signal('');

  readonly ventas = signal<VentaDto[]>([]);
  readonly clientes = signal<ClienteDto[]>([]);
  readonly tiposDocumento = signal<TipoDocumentoDto[]>([]);
  readonly listasPrecio = signal<ListaPrecioDto[]>([]);
  readonly preciosProducto = signal<PrecioProductoDto[]>([]);
  readonly productos = signal<ProductoDto[]>([]);
  readonly productoUnidades = signal<ProductoUnidadDto[]>([]);
  readonly sucursales = signal<SucursalDto[]>([]);
  readonly inventarios = signal<InventarioSucursalDto[]>([]);
  readonly draftDetalles = signal<CrearDetalleVentaDto[]>([]);
  readonly detallesVentaSeleccionada = signal<DetalleVentaVm[]>([]);

  readonly selectedVentaId = signal<number | null>(null);
  readonly selectedClienteId = signal<number | null>(null);
  readonly selectedListaPrecioId = signal<number | null>(null);
  readonly selectedPrecioProductoId = signal<number | null>(null);

  readonly currentUser = this.authSession.currentUser;
  readonly usuarioId = signal<number | null>(this.resolveUsuarioId());
  readonly usuarioNombre = signal(this.resolveUsuarioNombre());
  readonly sucursalId = signal<number | null>(this.resolveSucursalOperadorId());
  readonly sucursalNombre = signal(this.resolveSucursalOperadorNombre());
  readonly hasFixedSucursal = computed(() => this.sucursalId() !== null);

  readonly clientesActivos = computed(() => this.clientes().filter((item) => item.activo));
  readonly tiposDocumentoActivos = computed(() =>
    this.tiposDocumento().filter((item) => item.activo)
  );
  readonly listasPrecioActivas = computed(() =>
    this.listasPrecio().filter((item) => item.activa)
  );
  readonly productosActivos = computed(() => this.productos().filter((item) => item.activo));
  readonly productoUnidadesActivas = computed(() =>
    this.productoUnidades().filter((item) => item.activo)
  );
  readonly sucursalesActivas = computed(() =>
    this.sucursales().filter((item) => item.estado?.toLowerCase?.() !== 'inactiva')
  );

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
        label: `${item.unidad_medida?.nombre ?? 'Unidad'} (${item.unidad_medida?.simbolo ?? '-'})`
      }));
  }

  readonly ventasVm = computed<VentaVm[]>(() =>
    this.ventas().map((item) => ({
      ...item,
      cliente_nombre: item.cliente?.nombre ?? 'Venta de mostrador',
      lista_precio_nombre: this.getListaPrecioNombre(item.id_lista_precio),
      total_items: item.detalles?.length ?? 0
    }))
  );

  readonly preciosProductoVm = computed<PrecioProductoVm[]>(() =>
    this.preciosProducto().map((item) => ({
      ...item,
      producto_nombre: item.producto?.nombre ?? this.getProductoNombre(item.id_producto),
      codigo_producto: item.producto?.codigo ?? `PRD-${item.id_producto}`,
      lista_nombre: item.lista_precio?.nombre ?? this.getListaPrecioNombre(item.id_lista_precio)
    }))
  );

  readonly preciosListaSeleccionada = computed(() => {
    const idLista = this.selectedListaPrecioId();
    if (!idLista) {
      return this.preciosProductoVm();
    }

    return this.preciosProductoVm().filter((item) => item.id_lista_precio === idLista);
  });

  readonly historialVm = computed<VentaVm[]>(() => {
    const comprobante = this.historialForm.controls.comprobante.value.trim().toLowerCase();
    const idCliente = Number(this.historialForm.controls.id_cliente.value || 0);
    const idListaPrecio = Number(this.historialForm.controls.id_lista_precio.value || 0);
    const idSucursal = Number(this.historialForm.controls.id_sucursal.value || 0);
    const fechaDesde = this.historialForm.controls.fecha_desde.value;
    const fechaHasta = this.historialForm.controls.fecha_hasta.value;

    return this.ventasVm().filter((item) => {
      if (comprobante && !item.comprobante.toLowerCase().includes(comprobante)) {
        return false;
      }

      if (idCliente && item.id_cliente !== idCliente) {
        return false;
      }

      if (idListaPrecio && item.id_lista_precio !== idListaPrecio) {
        return false;
      }

      if (idSucursal && item.id_sucursal !== idSucursal) {
        return false;
      }

      if (fechaDesde && item.fecha && item.fecha.slice(0, 10) < fechaDesde) {
        return false;
      }

      if (fechaHasta && item.fecha && item.fecha.slice(0, 10) > fechaHasta) {
        return false;
      }

      return true;
    });
  });

  readonly selectedVenta = computed(() => {
    const idVenta = this.selectedVentaId();
    if (!idVenta) {
      return null;
    }

    return this.ventasVm().find((item) => item.id_venta === idVenta) ?? null;
  });

protected precioActualDetalle(): number | null {
  const idProducto = Number(this.detalleForm.controls.id_producto.value || 0);
  const idListaPrecio = Number(this.ventaForm.controls.id_lista_precio.value || 0);

  if (!idProducto || !idListaPrecio) {
    return null;
  }

  return this.getPrecioProductoActivo(idProducto, idListaPrecio)?.precio ?? null;
}

  protected stockDisponibleDetalle(): string {
    const idProducto = Number(this.detalleForm.controls.id_producto.value || 0);
    const idSucursal = Number(this.ventaForm.controls.id_sucursal.value || 0);
    const idProductoUnidad = Number(this.detalleForm.controls.id_producto_unidad.value || 0);

    if (!idProducto || !idSucursal || !idProductoUnidad) {
      return 'Sin inventario';
    }

    const disponible = this.getStockDisponibleEnUnidad(
      idProducto,
      idSucursal,
      idProductoUnidad
    );

    if (disponible === null) {
      return 'Sin inventario';
    }

    const unidad = this.getProductoUnidadById(idProductoUnidad);
    const simbolo = unidad?.unidad_medida?.simbolo ?? '';

    return `${disponible.toLocaleString('es-CO', {
      minimumFractionDigits: 0,
      maximumFractionDigits: 2
    })}${simbolo ? ` ${simbolo}` : ''}`;
  }

  readonly draftSubtotal = computed(() =>
    this.draftDetalles().reduce((acc, item) => {
      const precio = this.getPrecioUnitarioDraft(
        item.id_producto,
        Number(this.ventaForm.controls.id_lista_precio.value || 0)
      );
      return acc + item.cantidad * precio;
    }, 0)
  );
  readonly draftDescuentoTotal = computed(() =>
    this.draftDetalles().reduce((acc, item) => acc + (item.descuento ?? 0), 0)
  );
  readonly draftTotal = computed(() => this.draftSubtotal() - this.draftDescuentoTotal());

  readonly totalVentas = computed(() => this.ventasVm().length);
  readonly ventasDelDia = computed(() => {
    const hoy = new Date().toISOString().slice(0, 10);
    return this.ventasVm().filter((item) => item.fecha?.slice(0, 10) === hoy).length;
  });
  readonly totalClientes = computed(() => this.clientesActivos().length);
  readonly totalListasActivas = computed(() => this.listasPrecioActivas().length);

  readonly ventaForm = this.fb.nonNullable.group({
    id_cliente: [0],
    id_sucursal: [this.resolveSucursalOperadorId() ?? 0, [Validators.required, Validators.min(1)]],
    id_usuario: [this.resolveUsuarioId() ?? 0, [Validators.required, Validators.min(1)]],
    id_lista_precio: [0, [Validators.required, Validators.min(1)]]
  });

  readonly detalleForm = this.fb.nonNullable.group({
    id_producto: [0, [Validators.required, Validators.min(1)]],
    id_producto_unidad: [0, [Validators.required, Validators.min(1)]],
    cantidad: [1, [Validators.required, Validators.min(0.01)]],
    descuento: [0, [Validators.min(0)]]
  });

  readonly clienteForm = this.fb.nonNullable.group({
    id_tipo_documento: [0, [Validators.required, Validators.min(1)]],
    numero_documento: ['', [Validators.required, Validators.maxLength(40)]],
    nombre: ['', [Validators.required, Validators.maxLength(120)]],
    correo: [''],
    telefono: ['']
  });

  readonly listaPrecioForm = this.fb.nonNullable.group({
    nombre: ['', [Validators.required, Validators.maxLength(120)]],
    descripcion: ['']
  });

  readonly precioProductoForm = this.fb.nonNullable.group({
    id_producto: [0, [Validators.required, Validators.min(1)]],
    id_lista_precio: [0, [Validators.required, Validators.min(1)]],
    precio: [0, [Validators.required, Validators.min(0.01)]],
    fecha_vigencia: ['']
  });

  readonly historialForm = this.fb.nonNullable.group({
    comprobante: [''],
    id_cliente: [0],
    id_lista_precio: [0],
    id_sucursal: [this.resolveSucursalOperadorId() ?? 0],
    fecha_desde: [''],
    fecha_hasta: ['']
  });

  ngOnInit(): void {
    this.cargarVista();

    this.detalleForm.controls.id_producto.valueChanges
      .pipe(takeUntilDestroyed(this.destroyRef))
      .subscribe((idProducto) => {
        const productoId = Number(idProducto || 0);

        const unidades = this.productoUnidadesActivas().filter(
          (item) => Number(item.id_producto) === productoId
        );

        this.detalleForm.controls.id_producto_unidad.setValue(
          Number(unidades[0]?.id_producto_unidad ?? 0),
          { emitEvent: false }
        );
      });

    this.ventaForm.controls.id_lista_precio.valueChanges
      .pipe(takeUntilDestroyed(this.destroyRef))
      .subscribe(() => this.sincronizarDetalleVenta());

    this.ventaForm.controls.id_sucursal.valueChanges
      .pipe(takeUntilDestroyed(this.destroyRef))
      .subscribe(() => this.sincronizarDetalleVenta());
  }

  seleccionarSeccion(section: VentasSection): void {
    this.activeSection.set(section);
    this.errorMessage.set('');
    this.successMessage.set('');
  }

  cargarVista(): void {
    this.loading.set(true);
    this.errorMessage.set('');

    forkJoin({
      ventasResponse: this.ventasApi.venta.listarVentas({ 
        id_sucursal: this.resolveSucursalOperadorId() ?? undefined 
      }),
      clientesResponse: this.ventasApi.clientes.listarClientes(),
      tiposDocumentoResponse: this.ventasApi.tiposDocumento.listarTiposDocumento(),
      listasPrecioResponse: this.inventarioApi.listasPrecio.listarListasPrecio(),
      preciosProductoResponse: this.inventarioApi.preciosProducto.listarPreciosProducto(),
      productosResponse: this.inventarioApi.productos.listarProductos(),
      productoUnidadesResponse: this.inventarioApi.productoUnidades.listarProductoUnidades(),
      sucursalesResponse: this.sucursalesApi.listarSucursales().pipe(catchError(() => of([] as SucursalDto[]))),
      inventariosResponse: this.inventarioApi.inventarioSucursal.listarInventarioSucursal()
    })
      .pipe(
        finalize(() => this.loading.set(false)),
        takeUntilDestroyed(this.destroyRef)
      )
      .subscribe({
        next: ({
          ventasResponse,
          clientesResponse,
          tiposDocumentoResponse,
          listasPrecioResponse,
          preciosProductoResponse,
          productosResponse,
          productoUnidadesResponse,
          sucursalesResponse,
          inventariosResponse
        }) => {
          const ventas = this.extractData<VentaDto[]>(ventasResponse);
          this.ventas.set(ventas);
          this.clientes.set(this.extractData<ClienteDto[]>(clientesResponse));
          this.tiposDocumento.set(this.extractData<TipoDocumentoDto[]>(tiposDocumentoResponse));
          this.listasPrecio.set(this.extractData<ListaPrecioDto[]>(listasPrecioResponse));
          this.preciosProducto.set(this.extractData<PrecioProductoDto[]>(preciosProductoResponse));
          this.productos.set(this.extractData<ProductoDto[]>(productosResponse));
          this.productoUnidades.set(
            this.extractData<ProductoUnidadDto[]>(productoUnidadesResponse)
          );
          this.sucursales.set(this.extractData<SucursalDto[]>(sucursalesResponse));
          this.inventarios.set(this.extractData<InventarioSucursalDto[]>(inventariosResponse));
          this.ensureDefaults();

          const firstVenta = ventas[0];
          if (firstVenta) {
            this.seleccionarVenta(firstVenta.id_venta);
          } else {
            this.selectedVentaId.set(null);
            this.detallesVentaSeleccionada.set([]);
          }
        },
        error: (error: HttpErrorResponse) => {
          this.errorMessage.set(this.resolveApiError(error, 'No se pudo cargar el modulo de ventas.'));
          this.ventas.set([]);
          this.clientes.set([]);
          this.tiposDocumento.set([]);
          this.listasPrecio.set([]);
          this.preciosProducto.set([]);
          this.productos.set([]);
          this.productoUnidades.set([]);
          this.sucursales.set([]);
          this.inventarios.set([]);
          this.selectedVentaId.set(null);
          this.detallesVentaSeleccionada.set([]);
        }
      });
  }

  seleccionarVenta(idVenta: number): void {
    this.selectedVentaId.set(idVenta);
    this.cargarDetallesVenta(idVenta);
  }

  cargarDetallesVenta(idVenta: number): void {
    this.loadingDetalles.set(true);

    this.ventasApi.detallesVenta
      .listarDetallesPorVenta(idVenta)
      .pipe(
        finalize(() => this.loadingDetalles.set(false)),
        takeUntilDestroyed(this.destroyRef)
      )
      .subscribe({
        next: (response) => {
          this.detallesVentaSeleccionada.set(
            this.mapDetallesVenta(this.extractData<DetalleVentaDto[]>(response))
          );
        },
        error: () => {
          this.detallesVentaSeleccionada.set([]);
        }
      });
  }

  agregarDetalleVenta(): void {
    if (this.detalleForm.invalid) {
      this.detalleForm.markAllAsTouched();
      return;
    }

    const value = this.detalleForm.getRawValue();
    const idProducto = Number(value.id_producto);
    const idProductoUnidad = Number(value.id_producto_unidad);
    const idListaPrecio = Number(this.ventaForm.controls.id_lista_precio.value || 0);
    const idSucursal = Number(this.ventaForm.controls.id_sucursal.value || 0);
    const cantidad = Number(value.cantidad);

    const unidadSeleccionada = this.getProductoUnidadById(idProductoUnidad);
    const stockDisponibleBase = this.getStockDisponibleBase(idProducto, idSucursal);
    const cantidadActualDraftBase = this.getCantidadDraftEnBase(idProducto);
    const factorConversion = Number(unidadSeleccionada?.factor_conversion || 1);
    const cantidadSolicitadaBase = cantidad * factorConversion;

    if (!idListaPrecio || !this.getPrecioProductoActivo(idProducto, idListaPrecio)) {
      this.errorMessage.set('El producto no tiene precio activo en la lista seleccionada.');
      return;
    }

    if (!unidadSeleccionada) {
      this.errorMessage.set('El producto no tiene una unidad valida para la venta.');
      return;
    }

    if (stockDisponibleBase === null || stockDisponibleBase <= 0) {
      this.errorMessage.set('El producto no tiene stock disponible en la sucursal seleccionada.');
      return;
    }

    if (cantidadActualDraftBase + cantidadSolicitadaBase > stockDisponibleBase) {
      this.errorMessage.set('La cantidad supera el stock disponible de la sucursal seleccionada.');
      return;
    }

    const detalle: CrearDetalleVentaDto = {
      id_producto: idProducto,
      id_producto_unidad: idProductoUnidad,
      cantidad,
      descuento: Number(value.descuento || 0)
    };

    this.errorMessage.set('');
    this.draftDetalles.update((items) => [...items, detalle]);
    this.resetDetalleForm();
  }

  removerDetalleVenta(index: number): void {
    this.draftDetalles.update((items) => items.filter((_, itemIndex) => itemIndex !== index));
  }

  registrarVenta(): void {
    if (this.ventaForm.invalid) {
      this.ventaForm.markAllAsTouched();
      return;
    }

    if (!this.draftDetalles().length) {
      this.errorMessage.set('');
      void this.uiAlerts.warning('Agrega al menos un producto a la venta.');
      return;
    }

    this.submittingVenta.set(true);
    this.errorMessage.set('');
    this.successMessage.set('');

    const value = this.ventaForm.getRawValue();
    const payload: CrearVentaDto = {
      id_sucursal: Number(value.id_sucursal),
      id_usuario: Number(value.id_usuario),
      id_cliente: Number(value.id_cliente || 0) || null,
      id_lista_precio: Number(value.id_lista_precio),
      detalles: this.draftDetalles()
    };

    this.ventasApi.venta
      .crearVenta(payload)
      .pipe(
        finalize(() => this.submittingVenta.set(false)),
        takeUntilDestroyed(this.destroyRef)
      )
      .subscribe({
        next: (response) => {
          const venta = this.extractData<VentaDto>(response);
          this.successMessage.set('');
          void this.uiAlerts.successToast(
            `Venta registrada correctamente con comprobante ${venta.comprobante}.`
          );
          this.resetVentaForm();
          this.cargarVista();
          this.activeSection.set('ventas');
        },
        error: (error: HttpErrorResponse) => {
          this.errorMessage.set('');
          void this.uiAlerts.error(
            this.resolveApiError(error, 'No se pudo registrar la venta.')
          );
        }
      });
  }

  editarCliente(cliente: ClienteDto): void {
    this.activeSection.set('clientes');
    this.selectedClienteId.set(cliente.id_cliente);
    this.clienteForm.setValue({
      id_tipo_documento: cliente.id_tipo_documento,
      numero_documento: cliente.numero_documento,
      nombre: cliente.nombre,
      correo: cliente.correo ?? '',
      telefono: cliente.telefono ?? ''
    });
  }

  guardarCliente(): void {
    if (this.clienteForm.invalid) {
      this.clienteForm.markAllAsTouched();
      return;
    }

    this.submittingCliente.set(true);
    this.errorMessage.set('');
    this.successMessage.set('');

    const value = this.clienteForm.getRawValue();
    const clienteActual =
      this.clientes().find((item) => item.id_cliente === this.selectedClienteId()) ?? null;

    const payload: GuardarClienteDto = {
      id_tipo_documento: Number(value.id_tipo_documento),
      numero_documento: value.numero_documento.trim(),
      nombre: value.nombre.trim(),
      correo: value.correo.trim() || null,
      telefono: value.telefono.trim() || null,
      activo: clienteActual?.activo ?? true
    };

    const request = this.selectedClienteId()
      ? this.ventasApi.clientes.actualizarCliente(this.selectedClienteId()!, payload)
      : this.ventasApi.clientes.crearCliente(payload);

    request
      .pipe(
        finalize(() => this.submittingCliente.set(false)),
        takeUntilDestroyed(this.destroyRef)
      )
      .subscribe({
        next: () => {
          this.successMessage.set('');
          void this.uiAlerts.successToast(
            this.selectedClienteId()
              ? 'Cliente actualizado correctamente.'
              : 'Cliente creado correctamente.'
          );
          this.resetClienteForm();
          this.cargarVista();
          this.activeSection.set('clientes');
        },
        error: (error: HttpErrorResponse) => {
          this.errorMessage.set('');
          void this.uiAlerts.error(
            this.resolveApiError(error, 'No se pudo guardar el cliente.')
          );
        }
      });
  }

  async toggleEstadoCliente(cliente: ClienteDto): Promise<void> {
    const nextActivo = !cliente.activo;

    const confirmed = await this.uiAlerts.confirm({
      title: `${nextActivo ? 'Activar' : 'Desactivar'} cliente`,
      text: `Se actualizara el estado de "${cliente.nombre}".`,
      icon: 'warning',
      confirmButtonText: nextActivo ? 'Si, activar' : 'Si, desactivar'
    });

    if (!confirmed) {
      return;
    }

    const payload: GuardarClienteDto = {
      id_tipo_documento: cliente.id_tipo_documento,
      numero_documento: cliente.numero_documento,
      nombre: cliente.nombre,
      correo: cliente.correo,
      telefono: cliente.telefono,
      activo: nextActivo
    };

    this.ventasApi.clientes
      .actualizarCliente(cliente.id_cliente, payload)
      .pipe(takeUntilDestroyed(this.destroyRef))
      .subscribe({
        next: () => {
          this.successMessage.set('');
          void this.uiAlerts.successToast(
            nextActivo
              ? 'Cliente activado correctamente.'
              : 'Cliente desactivado correctamente.'
          );
          if (this.selectedClienteId() === cliente.id_cliente) {
            this.resetClienteForm();
          }
          this.cargarVista();
        },
        error: (error: HttpErrorResponse) => {
          this.errorMessage.set('');
          void this.uiAlerts.error(
            this.resolveApiError(error, 'No se pudo actualizar el cliente.')
          );
        }
      });
  }

  editarListaPrecio(lista: ListaPrecioDto): void {
    this.activeSection.set('precios');
    this.selectedListaPrecioId.set(lista.id_lista_precio);
    this.listaPrecioForm.setValue({
      nombre: lista.nombre,
      descripcion: lista.descripcion ?? ''
    });
    this.precioProductoForm.controls.id_lista_precio.setValue(lista.id_lista_precio);
  }

  guardarListaPrecio(): void {
    if (this.listaPrecioForm.invalid) {
      this.listaPrecioForm.markAllAsTouched();
      return;
    }

    this.submittingLista.set(true);
    this.errorMessage.set('');
    this.successMessage.set('');

    const value = this.listaPrecioForm.getRawValue();
    const listaActual =
      this.listasPrecio().find((item) => item.id_lista_precio === this.selectedListaPrecioId()) ??
      null;

    const payload: GuardarListaPrecioDto = {
      nombre: value.nombre.trim(),
      descripcion: value.descripcion.trim() || null,
      activa: listaActual?.activa ?? true
    };

    const request = this.selectedListaPrecioId()
      ? this.inventarioApi.listasPrecio.actualizarListaPrecio(this.selectedListaPrecioId()!, payload)
      : this.inventarioApi.listasPrecio.crearListaPrecio(payload);

    request
      .pipe(
        finalize(() => this.submittingLista.set(false)),
        takeUntilDestroyed(this.destroyRef)
      )
      .subscribe({
        next: () => {
          this.successMessage.set('');
          void this.uiAlerts.successToast(
            this.selectedListaPrecioId()
              ? 'Lista de precios actualizada correctamente.'
              : 'Lista de precios creada correctamente.'
          );
          this.resetListaPrecioForm();
          this.cargarVista();
          this.activeSection.set('precios');
        },
        error: (error: HttpErrorResponse) => {
          this.errorMessage.set('');
          void this.uiAlerts.error(
            this.resolveApiError(error, 'No se pudo guardar la lista de precios.')
          );
        }
      });
  }

  async toggleEstadoListaPrecio(lista: ListaPrecioDto): Promise<void> {
    const nextActiva = !lista.activa;

    const confirmed = await this.uiAlerts.confirm({
      title: `${nextActiva ? 'Activar' : 'Desactivar'} lista`,
      text: `Se actualizara el estado de "${lista.nombre}".`,
      icon: 'warning',
      confirmButtonText: nextActiva ? 'Si, activar' : 'Si, desactivar'
    });

    if (!confirmed) {
      return;
    }

    const payload: GuardarListaPrecioDto = {
      nombre: lista.nombre,
      descripcion: lista.descripcion,
      activa: nextActiva
    };

    this.inventarioApi.listasPrecio
      .actualizarListaPrecio(lista.id_lista_precio, payload)
      .pipe(takeUntilDestroyed(this.destroyRef))
      .subscribe({
        next: () => {
          this.successMessage.set('');
          void this.uiAlerts.successToast(
            nextActiva
              ? 'Lista de precios activada correctamente.'
              : 'Lista de precios desactivada correctamente.'
          );
          if (this.selectedListaPrecioId() === lista.id_lista_precio) {
            this.resetListaPrecioForm();
          }
          this.cargarVista();
        },
        error: (error: HttpErrorResponse) => {
          this.errorMessage.set('');
          void this.uiAlerts.error(
            this.resolveApiError(error, 'No se pudo actualizar la lista de precios.')
          );
        }
      });
  }

  editarPrecioProducto(precio: PrecioProductoDto): void {
    this.activeSection.set('precios');
    this.selectedPrecioProductoId.set(precio.id_precio_producto);
    this.selectedListaPrecioId.set(precio.id_lista_precio);
    this.precioProductoForm.setValue({
      id_producto: precio.id_producto,
      id_lista_precio: precio.id_lista_precio,
      precio: precio.precio,
      fecha_vigencia: precio.fecha_vigencia?.slice(0, 10) ?? ''
    });
  }

  guardarPrecioProducto(): void {
    if (this.precioProductoForm.invalid) {
      this.precioProductoForm.markAllAsTouched();
      return;
    }

    this.submittingPrecio.set(true);
    this.errorMessage.set('');
    this.successMessage.set('');

    const value = this.precioProductoForm.getRawValue();
    const precioActual =
      this.preciosProducto().find(
        (item) => item.id_precio_producto === this.selectedPrecioProductoId()
      ) ?? null;

    const payload = {
      id_producto: Number(value.id_producto),
      id_lista_precio: Number(value.id_lista_precio),
      precio: Number(value.precio),
      fecha_vigencia: value.fecha_vigencia || undefined,
      activo: precioActual?.activo ?? true
    };

    const request = this.selectedPrecioProductoId()
      ? this.inventarioApi.preciosProducto.actualizarPrecioProducto(
          this.selectedPrecioProductoId()!,
          payload
        )
      : this.inventarioApi.preciosProducto.crearPrecioProducto(payload);

    request
      .pipe(
        finalize(() => this.submittingPrecio.set(false)),
        takeUntilDestroyed(this.destroyRef)
      )
      .subscribe({
        next: () => {
          this.successMessage.set('');
          void this.uiAlerts.successToast(
            this.selectedPrecioProductoId()
              ? 'Precio de producto actualizado correctamente.'
              : 'Precio de producto creado correctamente.'
          );
          this.resetPrecioProductoForm();
          this.cargarVista();
          this.activeSection.set('precios');
        },
        error: (error: HttpErrorResponse) => {
          this.errorMessage.set('');
          void this.uiAlerts.error(
            this.resolveApiError(error, 'No se pudo guardar el precio del producto.')
          );
        }
      });
  }

  async toggleEstadoPrecioProducto(precio: PrecioProductoDto): Promise<void> {
    const nextActivo = !precio.activo;

    const confirmed = await this.uiAlerts.confirm({
      title: `${nextActivo ? 'Activar' : 'Desactivar'} precio`,
      text: `Se actualizara el precio del producto "${precio.producto?.nombre ?? `#${precio.id_producto}`}".`,
      icon: 'warning',
      confirmButtonText: nextActivo ? 'Si, activar' : 'Si, desactivar'
    });

    if (!confirmed) {
      return;
    }

    const payload = {
      id_producto: precio.id_producto,
      id_lista_precio: precio.id_lista_precio,
      precio: precio.precio,
      fecha_vigencia: precio.fecha_vigencia ?? undefined,
      activo: nextActivo
    };

    this.inventarioApi.preciosProducto
      .actualizarPrecioProducto(precio.id_precio_producto, payload)
      .pipe(takeUntilDestroyed(this.destroyRef))
      .subscribe({
        next: () => {
          this.successMessage.set('');
          void this.uiAlerts.successToast(
            nextActivo
              ? 'Precio activado correctamente.'
              : 'Precio desactivado correctamente.'
          );
          if (this.selectedPrecioProductoId() === precio.id_precio_producto) {
            this.resetPrecioProductoForm();
          }
          this.cargarVista();
        },
        error: (error: HttpErrorResponse) => {
          this.errorMessage.set('');
          void this.uiAlerts.error(
            this.resolveApiError(error, 'No se pudo actualizar el precio del producto.')
          );
        }
      });
  }

  aplicarFiltrosHistorial(): void {
    const firstVenta = this.historialVm()[0];
    if (firstVenta) {
      this.selectedVentaId.set(firstVenta.id_venta);
      this.cargarDetallesVenta(firstVenta.id_venta);
      return;
    }

    this.selectedVentaId.set(null);
    this.detallesVentaSeleccionada.set([]);
  }

  resetClienteForm(): void {
    this.selectedClienteId.set(null);
    this.clienteForm.reset({
      id_tipo_documento: this.tiposDocumentoActivos()[0]?.id_tipo_documento ?? 0,
      numero_documento: '',
      nombre: '',
      correo: '',
      telefono: ''
    });
  }

  resetListaPrecioForm(): void {
    this.selectedListaPrecioId.set(null);
    this.listaPrecioForm.reset({
      nombre: '',
      descripcion: ''
    });
  }

  resetPrecioProductoForm(): void {
    this.selectedPrecioProductoId.set(null);
    this.precioProductoForm.reset({
      id_producto: this.productosActivos()[0]?.id_producto ?? 0,
      id_lista_precio:
        this.selectedListaPrecioId() ?? this.listasPrecioActivas()[0]?.id_lista_precio ?? 0,
      precio: 0,
      fecha_vigencia: ''
    });
  }

  protected getProductoNombre(idProducto: number): string {
    return (
      this.productos().find((item) => item.id_producto === idProducto)?.nombre ??
      `Producto #${idProducto}`
    );
  }

  protected getUnidadNombre(idProductoUnidad: number): string {
    return (
      this.productoUnidades().find(
        (item) => Number(item.id_producto_unidad) === Number(idProductoUnidad)
      )?.unidad_medida?.nombre ?? `Unidad #${idProductoUnidad}`
    );
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

  protected getListaPrecioNombre(idListaPrecio: number | null | undefined): string {
    if (!idListaPrecio) {
      return 'Sin lista';
    }

    return (
      this.listasPrecio().find((item) => item.id_lista_precio === idListaPrecio)?.nombre ??
      `Lista #${idListaPrecio}`
    );
  }

  protected getPrecioUnitarioDraft(idProducto: number, idListaPrecio: number): number {
    return this.getPrecioProductoActivo(idProducto, idListaPrecio)?.precio ?? 0;
  }

  protected getSubtotalDraft(detalle: CrearDetalleVentaDto): number {
    const precio = this.getPrecioUnitarioDraft(
      detalle.id_producto,
      Number(this.ventaForm.controls.id_lista_precio.value || 0)
    );
    return detalle.cantidad * precio - (detalle.descuento ?? 0);
  }

  protected getStockDisponible(idProducto: number, idSucursal: number): number | null {
    return this.getStockDisponibleBase(idProducto, idSucursal);
  }

  protected getResponsableVenta(venta: VentaDto): string {
    if (venta.id_usuario === this.usuarioId()) {
      return this.usuarioNombre();
    }

    return `Usuario #${venta.id_usuario}`;
  }

protected productosDisponiblesVenta(): ProductoDto[] {
  const idSucursal = Number(this.ventaForm.controls.id_sucursal.value || 0);
  const idListaPrecio = Number(this.ventaForm.controls.id_lista_precio.value || 0);

  const productosConUnidad = new Set(
    this.productoUnidadesActivas().map((item) => Number(item.id_producto))
  );

  const productosConInventario = new Set(
    this.inventarios()
      .filter(
        (item) =>
          Number(item.id_sucursal) === idSucursal &&
          Number(item.cantidad_actual) > 0
      )
      .map((item) => Number(item.id_producto))
  );

  const productosConPrecio = new Set(
    this.preciosProducto()
      .filter(
        (item) =>
          item.activo &&
          Number(item.id_lista_precio) === idListaPrecio
      )
      .map((item) => Number(item.id_producto))
  );

  return this.productosActivos().filter(
    (item) =>
      productosConUnidad.has(Number(item.id_producto)) &&
      productosConInventario.has(Number(item.id_producto)) &&
      productosConPrecio.has(Number(item.id_producto))
  );
}

private getProductoUnidadById(
  idProductoUnidad: number
): ProductoUnidadDto | null {
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

private getStockDisponibleBase(
  idProducto: number,
  idSucursal: number
): number | null {
  return (
    this.getInventarioProductoSucursal(idProducto, idSucursal)?.cantidad_actual ?? null
  );
}

private getStockDisponibleEnUnidad(
  idProducto: number,
  idSucursal: number,
  idProductoUnidad: number
): number | null {
  const inventario = this.getInventarioProductoSucursal(idProducto, idSucursal);
  const productoUnidad = this.getProductoUnidadById(idProductoUnidad);

  if (!inventario || !productoUnidad) {
    return null;
  }

  const factor = Number(productoUnidad.factor_conversion || 1);

  if (factor <= 0) {
    return null;
  }

  return Number(inventario.cantidad_actual) / factor;
}

  private getCantidadDraftEnBase(idProducto: number): number {
    return this.draftDetalles()
      .filter((item) => Number(item.id_producto) === Number(idProducto))
      .reduce((acc, item) => {
        const unidad = this.getProductoUnidadById(Number(item.id_producto_unidad));
        const factor = Number(unidad?.factor_conversion || 1);
        return acc + Number(item.cantidad) * factor;
      }, 0);
  }

  private sincronizarDetalleVenta(): void {
    const productos = this.productosDisponiblesVenta();
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

  private ensureDefaults(): void {
    if (!this.ventaForm.controls.id_lista_precio.value && this.listasPrecioActivas().length) {
      this.ventaForm.controls.id_lista_precio.setValue(
        this.listasPrecioActivas()[0].id_lista_precio
      );
    }

    if (!this.clienteForm.controls.id_tipo_documento.value && this.tiposDocumentoActivos().length) {
      this.clienteForm.controls.id_tipo_documento.setValue(
        this.tiposDocumentoActivos()[0].id_tipo_documento
      );
    }

    if (!this.detalleForm.controls.id_producto.value && this.productosDisponiblesVenta().length) {
      this.resetDetalleForm();
    }

    if (!this.precioProductoForm.controls.id_producto.value && this.productosActivos().length) {
      this.resetPrecioProductoForm();
    }
  }

  private resetVentaForm(): void {
    this.ventaForm.reset({
      id_cliente: 0,
      id_sucursal: this.sucursalId() ?? 0,
      id_usuario: this.usuarioId() ?? 0,
      id_lista_precio: this.listasPrecioActivas()[0]?.id_lista_precio ?? 0
    });
    this.draftDetalles.set([]);
    this.resetDetalleForm();
  }

  private resetDetalleForm(): void {
    const firstProducto = this.productosDisponiblesVenta()[0];
    const firstUnidad = this.productoUnidadesActivas().find(
      (item) => Number(item.id_producto) === Number(firstProducto?.id_producto ?? 0)
    );

    this.detalleForm.reset({
      id_producto: Number(firstProducto?.id_producto ?? 0),
      id_producto_unidad: Number(firstUnidad?.id_producto_unidad ?? 0),
      cantidad: 1,
      descuento: 0
    });
  }

  private getPrecioProductoActivo(
    idProducto: number,
    idListaPrecio: number
  ): PrecioProductoDto | undefined {
    return this.preciosProducto().find(
      (item) =>
        Number(item.id_producto) === Number(idProducto) &&
        Number(item.id_lista_precio) === Number(idListaPrecio) &&
        item.activo
    );
  }

  private mapDetallesVenta(detalles: DetalleVentaDto[]): DetalleVentaVm[] {
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
        unidad:
          unidad?.unidad_medida?.nombre ??
          unidad?.unidad_medida?.simbolo ??
          `Unidad #${item.id_producto_unidad}`
      };
    });
  }

  private resolveApiError(error: HttpErrorResponse, fallback: string): string {
    const apiError = error.error as
      | {
          message?: string;
          errors?: Record<string, string>;
        }
      | null;

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

    return 'Usuario actual';
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

  descargarPdf(): void {
    const venta = this.selectedVenta();
    const detalles = this.detallesVentaSeleccionada();
    if (!venta) return;
    
    const responsable = this.getResponsableVenta(venta);
    const sucursal = this.getSucursalNombre(venta.id_sucursal);
    
    generarComprobanteVentaPdf(venta, detalles, sucursal, responsable);
  }
}
