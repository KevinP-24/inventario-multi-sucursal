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
import {
  AjustarInventarioDto,
  InventarioSucursalDto,
  StockAlertDto,
  TipoAjusteInventarioDto
} from '../../core/services/inventario/dtos/inventario-sucursal.dto';
import { MovimientoInventarioDto } from '../../core/services/inventario/dtos/movimiento-inventario.dto';
import { ProductoDto } from '../../core/services/inventario/dtos/producto.dto';

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

  readonly loading = signal(false);
  readonly loadingMovimientos = signal(false);
  readonly submitting = signal(false);
  readonly errorMessage = signal('');
  readonly successMessage = signal('');

  readonly inventarioBase = signal<InventarioFilaVm[]>([]);
  readonly inventarioVisible = signal<InventarioFilaVm[]>([]);
  readonly alertas = signal<StockAlertDto[]>([]);
  readonly movimientos = signal<MovimientoInventarioDto[]>([]);
  readonly selectedInventarioId = signal<number | null>(null);

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

  readonly filtroForm = this.fb.nonNullable.group({
    id_sucursal: this.resolveSucursalOperadorId() ?? 0,
    busqueda: '',
    solo_bajo_stock: false
  });

  readonly ajusteForm = this.fb.group({
    id_usuario: this.fb.nonNullable.control(this.resolveUsuarioId() ?? 0, [
      Validators.required,
      Validators.min(1)
    ]),
    tipo_ajuste: this.fb.nonNullable.control<TipoAjusteInventarioDto>('ENTRADA', [
      Validators.required
    ]),
    cantidad: this.fb.control<number | null>(1, [Validators.required, Validators.min(0.01)]),
    cantidad_actual_nueva: this.fb.control<number | null>(null)
  });

  ngOnInit(): void {
    this.cargarVista();

    this.ajusteForm.controls.tipo_ajuste.valueChanges
      .pipe(takeUntilDestroyed(this.destroyRef))
      .subscribe(tipo => this.syncValidacionesAjuste(tipo));

    this.syncValidacionesAjuste(this.ajusteForm.controls.tipo_ajuste.value);
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
      )
    })
      .pipe(
        finalize(() => this.loading.set(false)),
        takeUntilDestroyed(this.destroyRef)
      )
      .subscribe({
        next: ({ inventariosResponse, productosResponse, alertasResponse }) => {
          const inventarios = this.extractData<InventarioSucursalDto[]>(inventariosResponse);
          const productos = this.extractData<ProductoDto[]>(productosResponse);
          const alertas = this.extractData<StockAlertDto[]>(alertasResponse);

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
          this.aplicarFiltrosInternos();
        },
        error: () => {
          this.errorMessage.set('No se pudo cargar el módulo de inventario.');
          this.inventarioBase.set([]);
          this.inventarioVisible.set([]);
          this.alertas.set([]);
          this.movimientos.set([]);
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

  registrarAjuste(): void {
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

    if (this.ajusteForm.invalid) {
      this.ajusteForm.markAllAsTouched();
      return;
    }

    const payload = this.buildAjustePayload();
    if (!payload) {
      this.errorMessage.set('Completa correctamente los datos del movimiento.');
      return;
    }

    this.submitting.set(true);
    this.errorMessage.set('');
    this.successMessage.set('');

    this.inventarioApi.inventarioSucursal
      .ajustarInventarioSucursal(inventarioSeleccionado.id_inventario, payload)
      .pipe(
        finalize(() => this.submitting.set(false)),
        takeUntilDestroyed(this.destroyRef)
      )
      .subscribe({
        next: () => {
          this.successMessage.set('Movimiento registrado correctamente.');
          this.resetAjusteForm();
          this.cargarVista();
        },
        error: () => {
          this.errorMessage.set('No se pudo registrar el movimiento.');
        }
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
    const value = this.ajusteForm.getRawValue();

    if (value.tipo_ajuste === 'AJUSTE') {
      if (value.cantidad_actual_nueva === null || value.cantidad_actual_nueva === undefined) {
        return null;
      }

      return {
        id_usuario: Number(value.id_usuario),
        tipo_ajuste: value.tipo_ajuste,
        cantidad_actual_nueva: Number(value.cantidad_actual_nueva)
      };
    }

    if (value.cantidad === null || value.cantidad === undefined) {
      return null;
    }

    return {
      id_usuario: Number(value.id_usuario),
      tipo_ajuste: value.tipo_ajuste,
      cantidad: Number(value.cantidad)
    };
  }

  private syncValidacionesAjuste(tipo: TipoAjusteInventarioDto): void {
    const cantidadControl = this.ajusteForm.controls.cantidad;
    const cantidadNuevaControl = this.ajusteForm.controls.cantidad_actual_nueva;

    if (tipo === 'AJUSTE') {
      cantidadControl.clearValidators();
      cantidadControl.setValue(null, { emitEvent: false });

      cantidadNuevaControl.setValidators([Validators.required, Validators.min(0)]);
    } else {
      cantidadControl.setValidators([Validators.required, Validators.min(0.01)]);
      cantidadNuevaControl.clearValidators();
      cantidadNuevaControl.setValue(null, { emitEvent: false });
    }

    cantidadControl.updateValueAndValidity({ emitEvent: false });
    cantidadNuevaControl.updateValueAndValidity({ emitEvent: false });
  }

  private resetAjusteForm(): void {
    this.ajusteForm.patchValue({
      id_usuario: this.usuarioId() ?? 0,
      tipo_ajuste: 'ENTRADA',
      cantidad: 1,
      cantidad_actual_nueva: null
    });

    this.syncValidacionesAjuste('ENTRADA');
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