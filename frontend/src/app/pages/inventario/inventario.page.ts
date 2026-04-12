import { CommonModule } from '@angular/common';
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

import { PageHeaderComponent } from '../../shared/components/page-header/page-header.component';
import { InventarioApiService } from '../../core/services/inventario/inventario-api.service';
import { UiAlertService } from '../../core/services/ui-alert.service';
import {
  AjustarInventarioDto,
  InventarioSucursalDto,
  MovimientoOperativoInventarioDto,
  StockAlertDto,
  TipoAjusteInventarioDto
} from '../../core/services/inventario/dtos/inventario-sucursal.dto';
import { MovimientoInventarioDto } from '../../core/services/inventario/dtos/movimiento-inventario.dto';
import { GuardarProductoDto, ProductoDto } from '../../core/services/inventario/dtos/producto.dto';
import {
  GuardarProductoUnidadDto,
  ProductoUnidadDto
} from '../../core/services/inventario/dtos/producto-unidad.dto';
import { UnidadMedidaDto } from '../../core/services/inventario/dtos/unidad-medida.dto';

type InventarioSection = 'operacion' | 'productos' | 'unidades';
type MovimientoOperativoForm = 'AJUSTE' | 'DEVOLUCION' | 'MERMA';

interface InventarioFilaVm {
  readonly id_inventario: number;
  readonly id_sucursal: number;
  readonly id_producto: number;
  readonly cantidad_actual: number;
  readonly costo_promedio: number;
  readonly producto: string;
  readonly codigo_producto: string;
  readonly stock_minimo: number;
  readonly bajo_stock: boolean;
  readonly cantidad_faltante: number;
}

interface ProductoUnidadVm {
  readonly id_producto_unidad: number;
  readonly id_producto: number;
  readonly producto: string;
  readonly codigo_producto: string;
  readonly id_unidad: number;
  readonly unidad: string;
  readonly simbolo: string;
  readonly factor_conversion: number;
  readonly es_base: boolean;
  readonly activo: boolean;
}

@Component({
  selector: 'app-inventario-page',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, PageHeaderComponent],
  templateUrl: './inventario.page.html',
  styleUrl: './inventario.page.css',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class InventarioPage implements OnInit {
  private readonly fb = inject(FormBuilder);
  private readonly destroyRef = inject(DestroyRef);
  private readonly inventarioApi = inject(InventarioApiService);
  private readonly uiAlerts = inject(UiAlertService);

  readonly activeSection = signal<InventarioSection>('operacion');
  readonly loading = signal(false);
  readonly loadingMovimientos = signal(false);
  readonly submitting = signal(false);
  readonly submittingProducto = signal(false);
  readonly submittingUnidad = signal(false);
  readonly errorMessage = signal('');
  readonly successMessage = signal('');

  readonly inventarioBase = signal<InventarioFilaVm[]>([]);
  readonly inventarioVisible = signal<InventarioFilaVm[]>([]);
  readonly alertas = signal<StockAlertDto[]>([]);
  readonly movimientos = signal<MovimientoInventarioDto[]>([]);
  readonly productos = signal<ProductoDto[]>([]);
  readonly productoUnidades = signal<ProductoUnidadDto[]>([]);
  readonly unidadesMedida = signal<UnidadMedidaDto[]>([]);
  readonly selectedInventarioId = signal<number | null>(null);
  readonly selectedProductoId = signal<number | null>(null);
  readonly selectedProductoUnidadId = signal<number | null>(null);

  readonly operadorSucursalId = signal<number | null>(this.resolveSucursalOperadorId());
  readonly usuarioId = signal<number | null>(this.resolveUsuarioId());

  readonly sucursalesDisponibles = computed(() => {
    const ids = [...new Set(this.inventarioBase().map(item => item.id_sucursal))];
    return ids.sort((a, b) => a - b);
  });

  readonly inventarioSeleccionado = computed(() => {
    const id = this.selectedInventarioId();
    if (id === null) {
      return null;
    }

    return this.inventarioBase().find(item => item.id_inventario === id) ?? null;
  });

  readonly puedeOperarInventarioSeleccionado = computed(() => {
    const selected = this.inventarioSeleccionado();
    const sucursalOperador = this.operadorSucursalId();

    if (!selected) {
      return false;
    }

    if (sucursalOperador === null) {
      return true;
    }

    return selected.id_sucursal === sucursalOperador;
  });

  readonly totalReferencias = computed(() => this.inventarioVisible().length);

  readonly totalUnidades = computed(() =>
    this.inventarioVisible().reduce((acc, item) => acc + item.cantidad_actual, 0)
  );

  readonly totalBajoStock = computed(() =>
    this.inventarioVisible().filter(item => item.bajo_stock).length
  );

  readonly productosActivos = computed(() => this.productos().filter(item => item.activo));
  readonly productoStatusFilter = signal<'TODOS' | 'ACTIVOS' | 'INACTIVOS'>('TODOS');
  readonly productoSearchTerm = signal('');
  readonly productosCatalogoVisible = computed(() => {
    const status = this.productoStatusFilter();
    const search = this.productoSearchTerm().trim().toLowerCase();

    return this.productos().filter(item => {
      const matchStatus =
        status === 'TODOS' ||
        (status === 'ACTIVOS' && item.activo) ||
        (status === 'INACTIVOS' && !item.activo);

      const matchSearch =
        !search ||
        item.codigo.toLowerCase().includes(search) ||
        item.nombre.toLowerCase().includes(search);

      return matchStatus && matchSearch;
    });
  });

  readonly productoUnidadesVm = computed<ProductoUnidadVm[]>(() => {
    const productosMap = new Map(this.productos().map(item => [item.id_producto, item]));
    const unidadesMap = new Map(this.unidadesMedida().map(item => [item.id_unidad, item]));

    return this.productoUnidades().map(item => {
      const producto = item.producto ?? productosMap.get(item.id_producto) ?? null;
      const unidad = item.unidad_medida ?? unidadesMap.get(item.id_unidad) ?? null;

      return {
        id_producto_unidad: item.id_producto_unidad,
        id_producto: item.id_producto,
        producto: producto?.nombre ?? `Producto #${item.id_producto}`,
        codigo_producto: producto?.codigo ?? `PRD-${item.id_producto}`,
        id_unidad: item.id_unidad,
        unidad: unidad?.nombre ?? `Unidad #${item.id_unidad}`,
        simbolo: unidad?.simbolo ?? '-',
        factor_conversion: item.factor_conversion,
        es_base: item.es_base,
        activo: item.activo
      };
    });
  });

  readonly filtroForm = this.fb.nonNullable.group({
    id_sucursal: this.resolveSucursalOperadorId() ?? 0,
    busqueda: '',
    solo_bajo_stock: false
  });

  readonly movimientoForm = this.fb.group({
    id_usuario: this.fb.nonNullable.control(this.resolveUsuarioId() ?? 0, [
      Validators.required,
      Validators.min(1)
    ]),
    tipo_operacion: this.fb.nonNullable.control<MovimientoOperativoForm>('AJUSTE', [
      Validators.required
    ]),
    tipo_ajuste: this.fb.nonNullable.control<TipoAjusteInventarioDto>('ENTRADA', [
      Validators.required
    ]),
    cantidad: this.fb.control<number | null>(1, [Validators.required, Validators.min(0.01)]),
    cantidad_actual_nueva: this.fb.control<number | null>(null),
    id_origen: this.fb.control<number | null>(null),
    motivo: this.fb.control<string>('Ajuste operativo de inventario')
  });

  readonly productoForm = this.fb.nonNullable.group({
    codigo: ['', [Validators.required, Validators.maxLength(50)]],
    nombre: ['', [Validators.required, Validators.maxLength(120)]],
    descripcion: [''],
    stock_minimo: [0, [Validators.required, Validators.min(0)]]
  });

  readonly productoUnidadForm = this.fb.nonNullable.group({
    id_producto: [0, [Validators.required, Validators.min(1)]],
    id_unidad: [0, [Validators.required, Validators.min(1)]],
    factor_conversion: [1, [Validators.required, Validators.min(0.0001)]],
    es_base: [false]
  });

  ngOnInit(): void {
    this.cargarVista();

    this.movimientoForm.controls.tipo_operacion.valueChanges
      .pipe(takeUntilDestroyed(this.destroyRef))
      .subscribe(tipoOperacion => {
        this.syncValidacionesMovimiento(tipoOperacion, this.movimientoForm.controls.tipo_ajuste.value);
        this.syncMotivoPorOperacion(tipoOperacion);
      });

    this.movimientoForm.controls.tipo_ajuste.valueChanges
      .pipe(takeUntilDestroyed(this.destroyRef))
      .subscribe(tipoAjuste =>
        this.syncValidacionesMovimiento(this.movimientoForm.controls.tipo_operacion.value, tipoAjuste)
      );

    this.syncValidacionesMovimiento(
      this.movimientoForm.controls.tipo_operacion.value,
      this.movimientoForm.controls.tipo_ajuste.value
    );
  }

  seleccionarSeccion(section: InventarioSection): void {
    this.activeSection.set(section);
    this.errorMessage.set('');
    this.successMessage.set('');
  }

  setProductoStatusFilter(status: 'TODOS' | 'ACTIVOS' | 'INACTIVOS'): void {
    this.productoStatusFilter.set(status);
  }

  setProductoSearchTerm(term: string): void {
    this.productoSearchTerm.set(term);
  }

  cargarVista(): void {
    this.loading.set(true);
    this.errorMessage.set('');
    this.successMessage.set('');

    const idSucursalFiltro = this.filtroForm.controls.id_sucursal.value || null;

    forkJoin({
      inventariosResponse: this.inventarioApi.inventarioSucursal.listarInventarioSucursal(),
      productosResponse: this.inventarioApi.productos.listarProductos(),
      alertasResponse: this.inventarioApi.inventarioSucursal.listarAlertasStockBajo(
        idSucursalFiltro
      ),
      productoUnidadesResponse: this.inventarioApi.productoUnidades.listarProductoUnidades(),
      unidadesResponse: this.inventarioApi.unidadesMedida.listarUnidadesMedida()
    })
      .pipe(
        finalize(() => this.loading.set(false)),
        takeUntilDestroyed(this.destroyRef)
      )
      .subscribe({
        next: ({
          inventariosResponse,
          productosResponse,
          alertasResponse,
          productoUnidadesResponse,
          unidadesResponse
        }) => {
          const inventarios = this.extractData<InventarioSucursalDto[]>(inventariosResponse);
          const productos = this.extractData<ProductoDto[]>(productosResponse);
          const alertas = this.extractData<StockAlertDto[]>(alertasResponse);
          const productoUnidades =
            this.extractData<ProductoUnidadDto[]>(productoUnidadesResponse);
          const unidades = this.extractData<UnidadMedidaDto[]>(unidadesResponse);

          const productosMap = new Map<number, ProductoDto>(
            productos.map(producto => [producto.id_producto, producto])
          );

          const alertasMap = new Map<number, StockAlertDto>(
            alertas.map(alerta => [alerta.id_inventario, alerta])
          );

          const inventarioVm: InventarioFilaVm[] = inventarios.map(item => {
            const producto = productosMap.get(item.id_producto);
            const alerta = alertasMap.get(item.id_inventario);

            return {
              id_inventario: item.id_inventario,
              id_sucursal: item.id_sucursal,
              id_producto: item.id_producto,
              cantidad_actual: item.cantidad_actual,
              costo_promedio: item.costo_promedio,
              producto: producto?.nombre ?? alerta?.producto ?? `Producto #${item.id_producto}`,
              codigo_producto:
                producto?.codigo ?? alerta?.codigo_producto ?? `PRD-${item.id_producto}`,
              stock_minimo: alerta?.stock_minimo ?? producto?.stock_minimo ?? 0,
              bajo_stock: Boolean(alerta),
              cantidad_faltante: alerta?.cantidad_faltante ?? 0
            };
          });

          this.inventarioBase.set(inventarioVm);
          this.alertas.set(alertas);
          this.productos.set(productos);
          this.productoUnidades.set(productoUnidades);
          this.unidadesMedida.set(unidades.filter(item => item.activo));
          this.ensureUnidadFormDefaults();
          this.aplicarFiltrosInternos();
        },
        error: () => {
          this.errorMessage.set('No se pudo cargar el módulo de inventario.');
          this.inventarioBase.set([]);
          this.inventarioVisible.set([]);
          this.alertas.set([]);
          this.movimientos.set([]);
          this.productos.set([]);
          this.productoUnidades.set([]);
          this.unidadesMedida.set([]);
          this.selectedInventarioId.set(null);
        }
      });
  }

  aplicarFiltros(): void {
    this.errorMessage.set('');
    this.successMessage.set('');
    this.aplicarFiltrosInternos();
  }

  seleccionarInventario(idInventario: number): void {
    this.selectedInventarioId.set(idInventario);
    this.successMessage.set('');
    this.errorMessage.set('');
    this.cargarMovimientos(idInventario);
  }

  cargarMovimientos(idInventario: number): void {
    this.loadingMovimientos.set(true);

    this.inventarioApi.movimientosInventario
      .listarMovimientosPorInventario(idInventario)
      .pipe(
        finalize(() => this.loadingMovimientos.set(false)),
        takeUntilDestroyed(this.destroyRef)
      )
      .subscribe({
        next: response => {
          const movimientos = this.extractData<MovimientoInventarioDto[]>(response);
          this.movimientos.set(movimientos);
        },
        error: () => {
          this.movimientos.set([]);
        }
      });
  }

  registrarMovimiento(): void {
    const inventarioSeleccionado = this.inventarioSeleccionado();

    if (!inventarioSeleccionado) {
      this.errorMessage.set('Debes seleccionar un inventario.');
      return;
    }

    if (!this.puedeOperarInventarioSeleccionado()) {
      this.errorMessage.set(
        'Solo puedes registrar movimientos sobre el inventario de tu propia sucursal.'
      );
      return;
    }

    if (this.movimientoForm.invalid) {
      this.movimientoForm.markAllAsTouched();
      return;
    }

    const { tipo_operacion } = this.movimientoForm.getRawValue();

    this.submitting.set(true);
    this.errorMessage.set('');
    this.successMessage.set('');

    if (tipo_operacion === 'AJUSTE') {
      const payload = this.buildAjustePayload();
      if (!payload) {
        this.submitting.set(false);
        this.errorMessage.set('Completa correctamente los datos del ajuste.');
        return;
      }

      this.inventarioApi.inventarioSucursal
        .ajustarInventarioSucursal(inventarioSeleccionado.id_inventario, payload)
        .pipe(
          finalize(() => this.submitting.set(false)),
          takeUntilDestroyed(this.destroyRef)
        )
        .subscribe({
          next: () => {
            this.successMessage.set('Ajuste registrado correctamente.');
            this.resetMovimientoForm();
            this.cargarVista();
          },
          error: () => {
            this.errorMessage.set('No se pudo registrar el ajuste.');
          }
        });

      return;
    }

    const payload = this.buildMovimientoOperativoPayload();
    if (!payload) {
      this.submitting.set(false);
      this.errorMessage.set('Completa correctamente los datos del movimiento.');
      return;
    }

    const request =
      tipo_operacion === 'DEVOLUCION'
        ? this.inventarioApi.inventarioSucursal.registrarDevolucionInventario(
            inventarioSeleccionado.id_inventario,
            payload
          )
        : this.inventarioApi.inventarioSucursal.registrarMermaInventario(
            inventarioSeleccionado.id_inventario,
            payload
          );

    request
      .pipe(
        finalize(() => this.submitting.set(false)),
        takeUntilDestroyed(this.destroyRef)
      )
      .subscribe({
        next: () => {
          this.successMessage.set(
            tipo_operacion === 'DEVOLUCION'
              ? 'Devolución registrada correctamente.'
              : 'Merma registrada correctamente.'
          );
          this.resetMovimientoForm();
          this.cargarVista();
        },
        error: () => {
          this.errorMessage.set(
            tipo_operacion === 'DEVOLUCION'
              ? 'No se pudo registrar la devolución.'
              : 'No se pudo registrar la merma.'
          );
        }
      });
  }

  editarProducto(producto: ProductoDto): void {
    this.activeSection.set('productos');
    this.selectedProductoId.set(producto.id_producto);
    this.productoForm.setValue({
      codigo: producto.codigo,
      nombre: producto.nombre,
      descripcion: producto.descripcion ?? '',
      stock_minimo: producto.stock_minimo
    });
  }

  guardarProducto(): void {
    if (this.productoForm.invalid) {
      this.productoForm.markAllAsTouched();
      return;
    }

    this.submittingProducto.set(true);
    this.errorMessage.set('');
    this.successMessage.set('');

    const value = this.productoForm.getRawValue();
    const productoActual =
      this.productos().find(item => item.id_producto === this.selectedProductoId()) ?? null;
    const payload: GuardarProductoDto = {
      codigo: value.codigo.trim(),
      nombre: value.nombre.trim(),
      descripcion: value.descripcion.trim() || null,
      stock_minimo: Number(value.stock_minimo),
      activo: productoActual?.activo ?? true
    };

    const request = this.selectedProductoId()
      ? this.inventarioApi.productos.actualizarProducto(this.selectedProductoId()!, payload)
      : this.inventarioApi.productos.crearProducto(payload);

    request
      .pipe(
        finalize(() => this.submittingProducto.set(false)),
        takeUntilDestroyed(this.destroyRef)
      )
      .subscribe({
        next: () => {
          this.successMessage.set(
            this.selectedProductoId()
              ? 'Producto actualizado correctamente.'
              : 'Producto creado correctamente.'
          );
          this.resetProductoForm();
          this.cargarVista();
          this.activeSection.set('productos');
        },
        error: () => {
          this.errorMessage.set('No se pudo guardar el producto.');
        }
      });
  }

  async toggleEstadoProducto(producto: ProductoDto): Promise<void> {
    const nextActivo = !producto.activo;

    const confirmed = await this.uiAlerts.confirm({
      title: `${nextActivo ? 'Activar' : 'Desactivar'} producto`,
      text: `Se actualizara el estado de "${producto.nombre}".`,
      icon: 'warning',
      confirmButtonText: nextActivo ? 'Si, activar' : 'Si, desactivar'
    });

    if (!confirmed) {
      return;
    }

    const payload: GuardarProductoDto = {
      codigo: producto.codigo,
      nombre: producto.nombre,
      descripcion: producto.descripcion,
      stock_minimo: producto.stock_minimo,
      activo: nextActivo
    };

    this.inventarioApi.productos
      .actualizarProducto(producto.id_producto, payload)
      .pipe(takeUntilDestroyed(this.destroyRef))
      .subscribe({
        next: () => {
          this.successMessage.set(
            nextActivo ? 'Producto activado correctamente.' : 'Producto desactivado correctamente.'
          );
          if (this.selectedProductoId() === producto.id_producto) {
            this.resetProductoForm();
          }
          this.cargarVista();
          this.activeSection.set('productos');
        },
        error: () => {
          this.errorMessage.set(
            nextActivo ? 'No se pudo activar el producto.' : 'No se pudo desactivar el producto.'
          );
        }
      });
  }

  resetProductoForm(): void {
    this.selectedProductoId.set(null);
    this.productoForm.reset({
      codigo: '',
      nombre: '',
      descripcion: '',
      stock_minimo: 0
    });
  }

  editarProductoUnidad(item: ProductoUnidadVm): void {
    this.activeSection.set('unidades');
    this.selectedProductoUnidadId.set(item.id_producto_unidad);
    this.productoUnidadForm.setValue({
      id_producto: item.id_producto,
      id_unidad: item.id_unidad,
      factor_conversion: item.factor_conversion,
      es_base: item.es_base
    });
  }

  guardarProductoUnidad(): void {
    if (this.productoUnidadForm.invalid) {
      this.productoUnidadForm.markAllAsTouched();
      return;
    }

    this.submittingUnidad.set(true);
    this.errorMessage.set('');
    this.successMessage.set('');

    const value = this.productoUnidadForm.getRawValue();
    const unidadActual =
      this.productoUnidades().find(item => item.id_producto_unidad === this.selectedProductoUnidadId()) ??
      null;
    const payload: GuardarProductoUnidadDto = {
      id_producto: Number(value.id_producto),
      id_unidad: Number(value.id_unidad),
      factor_conversion: Number(value.factor_conversion),
      es_base: Boolean(value.es_base),
      activo: unidadActual?.activo ?? true
    };

    const request = this.selectedProductoUnidadId()
      ? this.inventarioApi.productoUnidades.actualizarProductoUnidad(
          this.selectedProductoUnidadId()!,
          payload
        )
      : this.inventarioApi.productoUnidades.crearProductoUnidad(payload);

    request
      .pipe(
        finalize(() => this.submittingUnidad.set(false)),
        takeUntilDestroyed(this.destroyRef)
      )
      .subscribe({
        next: () => {
          this.successMessage.set(
            this.selectedProductoUnidadId()
              ? 'Unidad del producto actualizada correctamente.'
              : 'Unidad del producto registrada correctamente.'
          );
          this.resetProductoUnidadForm();
          this.cargarVista();
          this.activeSection.set('unidades');
        },
        error: () => {
          this.errorMessage.set('No se pudo guardar la unidad del producto.');
        }
      });
  }

  async eliminarProductoUnidad(item: ProductoUnidadVm): Promise<void> {
    const nextActivo = !item.activo;

    const confirmed = await this.uiAlerts.confirm({
      title: `${nextActivo ? 'Activar' : 'Desactivar'} unidad`,
      text: `Se actualizara la unidad "${item.unidad}" del producto "${item.producto}".`,
      icon: 'warning',
      confirmButtonText: nextActivo ? 'Si, activar' : 'Si, desactivar'
    });

    if (!confirmed) {
      return;
    }

    const payload: GuardarProductoUnidadDto = {
      id_producto: item.id_producto,
      id_unidad: item.id_unidad,
      factor_conversion: item.factor_conversion,
      es_base: item.es_base,
      activo: nextActivo
    };

    this.inventarioApi.productoUnidades
      .actualizarProductoUnidad(item.id_producto_unidad, payload)
      .pipe(takeUntilDestroyed(this.destroyRef))
      .subscribe({
        next: () => {
          this.successMessage.set(
            nextActivo
              ? 'Unidad del producto activada correctamente.'
              : 'Unidad del producto desactivada correctamente.'
          );
          if (this.selectedProductoUnidadId() === item.id_producto_unidad) {
            this.resetProductoUnidadForm();
          }
          this.cargarVista();
          this.activeSection.set('unidades');
        },
        error: () => {
          this.errorMessage.set(
            nextActivo
              ? 'No se pudo activar la unidad del producto.'
              : 'No se pudo desactivar la unidad del producto.'
          );
        }
      });
  }

  resetProductoUnidadForm(): void {
    this.selectedProductoUnidadId.set(null);
    this.productoUnidadForm.reset({
      id_producto: this.productosActivos()[0]?.id_producto ?? 0,
      id_unidad: this.unidadesMedida()[0]?.id_unidad ?? 0,
      factor_conversion: 1,
      es_base: false
    });
  }

  private aplicarFiltrosInternos(): void {
    const idSucursal = Number(this.filtroForm.controls.id_sucursal.value || 0);
    const busqueda = this.filtroForm.controls.busqueda.value.trim().toLowerCase();
    const soloBajoStock = this.filtroForm.controls.solo_bajo_stock.value;

    const filtrado = this.inventarioBase().filter(item => {
      const matchSucursal = !idSucursal || item.id_sucursal === idSucursal;
      const matchBusqueda =
        !busqueda ||
        item.producto.toLowerCase().includes(busqueda) ||
        item.codigo_producto.toLowerCase().includes(busqueda);

      const matchStock = !soloBajoStock || item.bajo_stock;

      return matchSucursal && matchBusqueda && matchStock;
    });

    this.inventarioVisible.set(filtrado);

    if (!filtrado.length) {
      this.selectedInventarioId.set(null);
      this.movimientos.set([]);
      return;
    }

    const seleccionadoActual = filtrado.find(
      item => item.id_inventario === this.selectedInventarioId()
    );

    const target = seleccionadoActual ?? filtrado[0];
    this.selectedInventarioId.set(target.id_inventario);
    this.cargarMovimientos(target.id_inventario);
  }

  private buildAjustePayload(): AjustarInventarioDto | null {
    const value = this.movimientoForm.getRawValue();

    if (value.tipo_ajuste === 'AJUSTE') {
      if (value.cantidad_actual_nueva === null || value.cantidad_actual_nueva === undefined) {
        return null;
      }

      return {
        id_usuario: Number(value.id_usuario),
        tipo_ajuste: value.tipo_ajuste,
        cantidad_actual_nueva: Number(value.cantidad_actual_nueva),
        motivo: value.motivo?.trim() || null
      };
    }

    if (value.cantidad === null || value.cantidad === undefined) {
      return null;
    }

    return {
      id_usuario: Number(value.id_usuario),
      tipo_ajuste: value.tipo_ajuste,
      cantidad: Number(value.cantidad),
      motivo: value.motivo?.trim() || null
    };
  }

  private buildMovimientoOperativoPayload(): MovimientoOperativoInventarioDto | null {
    const value = this.movimientoForm.getRawValue();

    if (value.cantidad === null || value.cantidad === undefined) {
      return null;
    }

    return {
      id_usuario: Number(value.id_usuario),
      cantidad: Number(value.cantidad),
      id_origen:
        value.id_origen === null || value.id_origen === undefined ? null : Number(value.id_origen),
      motivo: value.motivo?.trim() || null
    };
  }

  private syncValidacionesMovimiento(
    tipoOperacion: MovimientoOperativoForm,
    tipoAjuste: TipoAjusteInventarioDto
  ): void {
    const cantidadControl = this.movimientoForm.controls.cantidad;
    const cantidadNuevaControl = this.movimientoForm.controls.cantidad_actual_nueva;
    const idOrigenControl = this.movimientoForm.controls.id_origen;

    if (tipoOperacion === 'AJUSTE' && tipoAjuste === 'AJUSTE') {
      cantidadControl.clearValidators();
      cantidadControl.setValue(null, { emitEvent: false });
      cantidadNuevaControl.setValidators([Validators.required, Validators.min(0)]);
    } else {
      cantidadControl.setValidators([Validators.required, Validators.min(0.01)]);
      if (cantidadControl.value === null) {
        cantidadControl.setValue(1, { emitEvent: false });
      }
      cantidadNuevaControl.clearValidators();
      cantidadNuevaControl.setValue(null, { emitEvent: false });
    }

    if (tipoOperacion === 'AJUSTE') {
      idOrigenControl.clearValidators();
      idOrigenControl.setValue(null, { emitEvent: false });
    } else {
      idOrigenControl.setValidators([Validators.min(1)]);
    }

    cantidadControl.updateValueAndValidity({ emitEvent: false });
    cantidadNuevaControl.updateValueAndValidity({ emitEvent: false });
    idOrigenControl.updateValueAndValidity({ emitEvent: false });
  }

  private syncMotivoPorOperacion(tipoOperacion: MovimientoOperativoForm): void {
    const motivoControl = this.movimientoForm.controls.motivo;

    if (motivoControl.dirty && motivoControl.value?.trim()) {
      return;
    }

    const defaultMotivo =
      tipoOperacion === 'DEVOLUCION'
        ? 'Devolución de inventario'
        : tipoOperacion === 'MERMA'
          ? 'Merma de inventario'
          : 'Ajuste operativo de inventario';

    motivoControl.setValue(defaultMotivo, { emitEvent: false });
  }

  private resetMovimientoForm(): void {
    this.movimientoForm.patchValue({
      id_usuario: this.usuarioId() ?? 0,
      tipo_operacion: 'AJUSTE',
      tipo_ajuste: 'ENTRADA',
      cantidad: 1,
      cantidad_actual_nueva: null,
      id_origen: null,
      motivo: 'Ajuste operativo de inventario'
    });

    this.syncValidacionesMovimiento('AJUSTE', 'ENTRADA');
  }

  private ensureUnidadFormDefaults(): void {
    const currentProducto = this.productoUnidadForm.controls.id_producto.value;
    const currentUnidad = this.productoUnidadForm.controls.id_unidad.value;

    if (!currentProducto && this.productosActivos().length) {
      this.productoUnidadForm.controls.id_producto.setValue(this.productosActivos()[0].id_producto);
    }

    if (!currentUnidad && this.unidadesMedida().length) {
      this.productoUnidadForm.controls.id_unidad.setValue(this.unidadesMedida()[0].id_unidad);
    }
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
    const keys = ['ms_user', 'auth_user', 'current_user'];

    for (const key of keys) {
      const raw = localStorage.getItem(key);
      if (!raw) {
        continue;
      }

      try {
        const parsed = JSON.parse(raw) as Record<string, unknown>;

        const idSucursal =
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
    const keys = ['ms_user', 'auth_user', 'current_user'];

    for (const key of keys) {
      const raw = localStorage.getItem(key);
      if (!raw) {
        continue;
      }

      try {
        const parsed = JSON.parse(raw) as Record<string, unknown>;

        const idUsuario =
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
}

