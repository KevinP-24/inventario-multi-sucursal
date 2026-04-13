import { CommonModule } from '@angular/common';
import {
  AfterViewInit,
  ChangeDetectionStrategy,
  Component,
  DestroyRef,
  ElementRef,
  OnInit,
  ViewChild,
  computed,
  effect,
  inject,
  signal
} from '@angular/core';
import { toSignal, takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { FormBuilder, ReactiveFormsModule } from '@angular/forms';
import { RouterLink } from '@angular/router';
import {
  ArcElement,
  BarController,
  BarElement,
  CategoryScale,
  Chart,
  Colors,
  DoughnutController,
  Legend,
  LineController,
  LineElement,
  LinearScale,
  PointElement,
  Tooltip
} from 'chart.js';
import { finalize, forkJoin, map, of, startWith, switchMap } from 'rxjs';

import { getNavigationItemsByRole } from '../../core/config/section-access.config';
import { NavigationItem } from '../../core/models/navigation-item.model';
import { AuthSessionService } from '../../core/services/auth/auth-session.service';
import { ComprasApiService } from '../../core/services/compras/compras-api.service';
import { OrdenCompraDto } from '../../core/services/compras/dtos/orden-compra.dto';
import { InventarioApiService } from '../../core/services/inventario/inventario-api.service';
import { InventarioSucursalDto } from '../../core/services/inventario/dtos/inventario-sucursal.dto';
import { ProductoDto } from '../../core/services/inventario/dtos/producto.dto';
import { ApiResponseDto } from '../../core/models/api-response.dto';
import { SucursalDto } from '../../core/services/sucursales/dtos/sucursal.dto';
import { SucursalesApiService } from '../../core/services/sucursales/sucursales-api.service';
import { DetalleTransferenciaDto } from '../../core/services/transferencias/dtos/detalle-transferencia.dto';
import { TransferenciaDto } from '../../core/services/transferencias/dtos/transferencia.dto';
import { TransferenciasApiService } from '../../core/services/transferencias/transferencias-api.service';
import { DetalleVentaDto } from '../../core/services/ventas/dtos/detalle-venta.dto';
import { VentaDto } from '../../core/services/ventas/dtos/venta.dto';
import { VentasApiService } from '../../core/services/ventas/ventas-api.service';
import { PageHeaderComponent } from '../../shared/components/page-header/page-header.component';

Chart.register(
  Colors,
  ArcElement,
  BarController,
  BarElement,
  CategoryScale,
  DoughnutController,
  Legend,
  LineController,
  LineElement,
  LinearScale,
  PointElement,
  Tooltip
);

type RoleCode = 'ADMIN_GENERAL' | 'ADMIN_SUCURSAL' | 'OPERARIO_INVENTARIO';

interface DashboardFocusItem {
  title: string;
  description: string;
}

interface DashboardViewModel {
  eyebrow: string;
  title: string;
  description: string;
  focus: DashboardFocusItem[];
}

interface ProductDemandVm {
  readonly id_producto: number;
  readonly nombre: string;
  readonly cantidad: number;
}

interface TransferImpactVm {
  readonly id_transferencia: number;
  readonly origen: string;
  readonly destino: string;
  readonly estado: string;
  readonly fecha: string | null;
  readonly cantidad: number;
  readonly impacto: string;
}

interface ReplenishmentVm {
  readonly id_inventario: number;
  readonly producto: string;
  readonly sucursal: string;
  readonly cantidad_actual: number;
  readonly stock_minimo: number;
  readonly faltante: number;
  readonly severidad: 'critico' | 'proximo';
}

interface BranchComparisonVm {
  readonly id_sucursal: number;
  readonly nombre: string;
  readonly ventas_total: number;
  readonly stock_total: number;
  readonly productos_criticos: number;
  readonly transferencias_activas: number;
}

interface SalesMonthVm {
  readonly label: string;
  readonly total: number;
}

const DASHBOARD_BY_ROLE: Record<RoleCode, DashboardViewModel> = {
  ADMIN_GENERAL: {
    eyebrow: 'Dashboard administrativo',
    title: 'Analisis transversal de la red multi-sucursal',
    description:
      'Supervisa ventas, inventario, transferencias y reabastecimiento con una lectura global de toda la operacion.',
    focus: [
      {
        title: 'Comparacion entre sucursales',
        description:
          'Detectar que sedes venden mejor, cuales tienen presion de stock y donde hay mas riesgo.'
      },
      {
        title: 'Seguimiento de transferencias',
        description:
          'Identificar operaciones vivas, impactos pendientes y movimientos que afectan el balance de la red.'
      },
      {
        title: 'Decision de abastecimiento',
        description:
          'Priorizar reabastecimiento segun ventas del periodo, criticidad y demanda real.'
      }
    ]
  },
  ADMIN_SUCURSAL: {
    eyebrow: 'Dashboard de sucursal',
    title: 'Indicadores operativos y administrativos de tu sucursal',
    description:
      'Consulta ventas, demanda, productos criticos y transferencias activas con foco en tu sede y su contexto operativo.',
    focus: [
      {
        title: 'Control de ventas',
        description:
          'Comparar el mes actual frente a periodos anteriores para detectar aceleracion o caida.'
      },
      {
        title: 'Riesgo de agotados',
        description:
          'Ver productos con rotacion alta y stock comprometido para actuar antes de un quiebre.'
      },
      {
        title: 'Seguimiento diario',
        description:
          'Revisar transferencias activas y su efecto en el inventario de la sucursal.'
      }
    ]
  },
  OPERARIO_INVENTARIO: {
    eyebrow: 'Dashboard operativo',
    title: 'Lectura rapida de la operacion del dia',
    description:
      'Concentra ventas recientes, demanda, transferencias activas y alertas de reabastecimiento para reaccionar rapido.',
    focus: [
      {
        title: 'Productos por atender',
        description:
          'Saber que se mueve mas, que casi no sale y que referencias necesitan reposicion.'
      },
      {
        title: 'Transferencias vivas',
        description:
          'Entender que movimientos siguen pendientes y como afectan el stock esperado.'
      },
      {
        title: 'Accion inmediata',
        description: 'Entrar a los modulos correctos desde el dashboard segun la prioridad del momento.'
      }
    ]
  }
};

@Component({
  selector: 'app-dashboard-page',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, RouterLink, PageHeaderComponent],
  templateUrl: './dashboard.page.html',
  styleUrl: './dashboard.page.css',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class DashboardPage implements OnInit, AfterViewInit {
  private readonly fb = inject(FormBuilder);
  private readonly destroyRef = inject(DestroyRef);
  private readonly authSession = inject(AuthSessionService);
  private readonly ventasApi = inject(VentasApiService);
  private readonly inventarioApi = inject(InventarioApiService);
  private readonly sucursalesApi = inject(SucursalesApiService);
  private readonly transferenciasApi = inject(TransferenciasApiService);
  private readonly comprasApi = inject(ComprasApiService);

  @ViewChild('salesChart') private salesChartRef?: ElementRef<HTMLCanvasElement>;
  @ViewChild('demandChart') private demandChartRef?: ElementRef<HTMLCanvasElement>;
  @ViewChild('transferChart') private transferChartRef?: ElementRef<HTMLCanvasElement>;
  @ViewChild('branchChart') private branchChartRef?: ElementRef<HTMLCanvasElement>;

  private salesChart?: Chart;
  private demandChart?: Chart;
  private transferChart?: Chart;
  private branchChart?: Chart;

  protected readonly currentUser = this.authSession.currentUser;
  protected readonly loading = signal(false);
  protected readonly errorMessage = signal('');

  protected readonly ventas = signal<VentaDto[]>([]);
  protected readonly inventarios = signal<InventarioSucursalDto[]>([]);
  protected readonly productos = signal<ProductoDto[]>([]);
  protected readonly sucursales = signal<SucursalDto[]>([]);
  protected readonly transferencias = signal<TransferenciaDto[]>([]);
  protected readonly compras = signal<OrdenCompraDto[]>([]);
  protected readonly ventaDetallesMap = signal<Record<number, DetalleVentaDto[]>>({});
  protected readonly transferenciaDetallesMap = signal<Record<number, DetalleTransferenciaDto[]>>(
    {}
  );

  protected readonly filterForm = this.fb.nonNullable.group({
    id_sucursal: [0],
    ventana_meses: [4]
  });

  private readonly filterState = toSignal(
    this.filterForm.valueChanges.pipe(startWith(this.filterForm.getRawValue())),
    { initialValue: this.filterForm.getRawValue() }
  );

  protected readonly roleCode = computed<RoleCode>(() => {
    const currentUser = this.currentUser();
    const roleCode = currentUser?.rol?.codigo?.trim?.().toUpperCase?.();

    if (
      roleCode === 'ADMIN_GENERAL' ||
      roleCode === 'ADMIN_SUCURSAL' ||
      roleCode === 'OPERARIO_INVENTARIO'
    ) {
      return roleCode;
    }

    const roleName = currentUser?.rol?.nombre?.trim?.().toLowerCase?.();

    if (roleName === 'administrador general') {
      return 'ADMIN_GENERAL';
    }

    if (roleName === 'administrador de sucursal' || roleName === 'admin sucursal') {
      return 'ADMIN_SUCURSAL';
    }

    if (roleName === 'operario de inventario' || roleName === 'operador de inventario') {
      return 'OPERARIO_INVENTARIO';
    }

    const roleId = currentUser?.id_rol ?? currentUser?.rol?.id_rol ?? null;

    if (roleId === 1) {
      return 'ADMIN_GENERAL';
    }

    if (roleId === 2) {
      return 'ADMIN_SUCURSAL';
    }

    if (roleId === 3) {
      return 'OPERARIO_INVENTARIO';
    }

    return 'OPERARIO_INVENTARIO';
  });

  protected readonly content = computed(() => DASHBOARD_BY_ROLE[this.roleCode()]);
  protected readonly shortcuts = computed<NavigationItem[]>(() =>
    getNavigationItemsByRole(this.roleCode()).filter(
      (item) => item.path !== '/app/dashboard' && item.path !== '/app/reportes'
    )
  );

  protected readonly fixedSucursalId = computed<number | null>(() => {
    if (this.roleCode() === 'ADMIN_GENERAL') {
      return null;
    }

    return this.currentUser()?.id_sucursal ?? this.currentUser()?.sucursal?.id_sucursal ?? null;
  });

  protected readonly selectedSucursalId = computed<number | null>(() => {
    const fixed = this.fixedSucursalId();
    if (fixed) {
      return fixed;
    }

    const selected = Number(this.filterState()?.id_sucursal || 0);
    return selected || null;
  });

  protected readonly selectedSucursalName = computed(() => {
    const idSucursal = this.selectedSucursalId();
    if (!idSucursal) {
      return 'Toda la red';
    }

    return this.getSucursalNombre(idSucursal);
  });

  protected readonly selectedWindowMonths = computed(() =>
    Number(this.filterState()?.ventana_meses || 4)
  );
  protected readonly canCompareBranches = computed(() => this.roleCode() !== 'OPERARIO_INVENTARIO');

  protected readonly ventasFiltradas = computed(() => {
    const idSucursal = this.selectedSucursalId();
    const cutoff = this.getWindowStartDate(this.selectedWindowMonths());

    return this.ventas().filter((item) => {
      if (idSucursal && item.id_sucursal !== idSucursal) {
        return false;
      }

      if (!item.fecha) {
        return false;
      }

      return new Date(item.fecha) >= cutoff;
    });
  });

  protected readonly inventariosFiltrados = computed(() => {
    const idSucursal = this.selectedSucursalId();
    return this.inventarios().filter((item) => !idSucursal || item.id_sucursal === idSucursal);
  });

  protected readonly transferenciasFiltradas = computed(() => {
    const idSucursal = this.selectedSucursalId();
    const cutoff = this.getWindowStartDate(this.selectedWindowMonths());

    return this.transferencias().filter((item) => {
      if (
        idSucursal &&
        item.id_sucursal_origen !== idSucursal &&
        item.id_sucursal_destino !== idSucursal
      ) {
        return false;
      }

      if (!item.fecha_solicitud) {
        return true;
      }

      return new Date(item.fecha_solicitud) >= cutoff;
    });
  });

  protected readonly salesMonths = computed<SalesMonthVm[]>(() => {
    const months = this.buildMonthBuckets(this.selectedWindowMonths());
    const totals = new Map<string, number>(months.map((item) => [item.key, 0]));

    this.ventasFiltradas().forEach((venta) => {
      if (!venta.fecha) {
        return;
      }

      const key = venta.fecha.slice(0, 7);
      totals.set(key, (totals.get(key) ?? 0) + venta.total);
    });

    return months.map((item) => ({
      label: item.label,
      total: totals.get(item.key) ?? 0
    }));
  });

  protected readonly currentMonthSales = computed(() => this.salesMonths().at(-1)?.total ?? 0);
  protected readonly previousMonthSales = computed(() => this.salesMonths().at(-2)?.total ?? 0);
  protected readonly currentMonthDelta = computed(() => {
    const previous = this.previousMonthSales();
    if (!previous) {
      return this.currentMonthSales() ? 100 : 0;
    }

    return ((this.currentMonthSales() - previous) / previous) * 100;
  });

  protected readonly demandByProduct = computed<ProductDemandVm[]>(() => {
    const totals = new Map<number, number>();

    this.ventasFiltradas().forEach((venta) => {
      const detalles = this.ventaDetallesMap()[venta.id_venta] ?? [];
      detalles.forEach((detalle) => {
        totals.set(detalle.id_producto, (totals.get(detalle.id_producto) ?? 0) + detalle.cantidad);
      });
    });

    return Array.from(totals.entries())
      .map(([id_producto, cantidad]) => ({
        id_producto,
        nombre: this.getProductoNombre(id_producto),
        cantidad
      }))
      .sort((a, b) => b.cantidad - a.cantidad);
  });

  protected readonly topDemandProducts = computed(() => this.demandByProduct().slice(0, 5));

  protected readonly lowDemandProducts = computed<ProductDemandVm[]>(() => {
    const totals = new Map<number, number>();

    this.inventariosFiltrados().forEach((item) => {
      totals.set(item.id_producto, 0);
    });

    this.demandByProduct().forEach((item) => {
      totals.set(item.id_producto, item.cantidad);
    });

    return Array.from(totals.entries())
      .map(([id_producto, cantidad]) => ({
        id_producto,
        nombre: this.getProductoNombre(id_producto),
        cantidad
      }))
      .sort((a, b) => a.cantidad - b.cantidad)
      .slice(0, 5);
  });

  protected readonly activeTransfers = computed<TransferImpactVm[]>(() => {
    return this.transferenciasFiltradas()
      .map((item) => {
        const estado = (item.estado ?? item.envio?.estado_envio ?? 'PENDIENTE').toUpperCase();
        const isActive = !['RECIBIDA', 'CERRADA', 'CANCELADA'].some((state) =>
          estado.includes(state)
        );

        if (!isActive) {
          return null;
        }

        const detalles = this.transferenciaDetallesMap()[item.id_transferencia] ?? [];
        const cantidad = detalles.reduce(
          (acc, detail) => acc + (detail.cantidad_aprobada || detail.cantidad_solicitada || 0),
          0
        );

        return {
          id_transferencia: item.id_transferencia,
          origen: this.getSucursalNombre(item.id_sucursal_origen),
          destino: this.getSucursalNombre(item.id_sucursal_destino),
          estado,
          fecha: item.envio?.fecha_envio ?? item.fecha_solicitud,
          cantidad,
          impacto: this.getTransferImpactLabel(item, cantidad)
        };
      })
      .filter((item): item is TransferImpactVm => item !== null)
      .slice(0, 8);
  });

  protected readonly transferStateSummary = computed(() => {
    const summary = new Map<string, number>();

    this.transferenciasFiltradas().forEach((item) => {
      const estado = (item.estado ?? item.envio?.estado_envio ?? 'Sin estado').toUpperCase();
      summary.set(estado, (summary.get(estado) ?? 0) + 1);
    });

    return Array.from(summary.entries()).map(([estado, total]) => ({ estado, total }));
  });

  protected readonly replenishmentAlerts = computed<ReplenishmentVm[]>(() => {
    return this.inventariosFiltrados()
      .filter((item) => this.getProductoStockMinimo(item.id_producto) > 0)
      .map((item) => {
        const stockMinimo = this.getProductoStockMinimo(item.id_producto);
        const faltante = stockMinimo - item.cantidad_actual;
        const porcentaje = item.cantidad_actual / stockMinimo;

        if (faltante > 0) {
          return {
            id_inventario: item.id_inventario,
            producto: this.getProductoNombre(item.id_producto),
            sucursal: this.getSucursalNombre(item.id_sucursal),
            cantidad_actual: item.cantidad_actual,
            stock_minimo: stockMinimo,
            faltante,
            severidad: 'critico' as const
          };
        }

        if (porcentaje <= 1.2) {
          return {
            id_inventario: item.id_inventario,
            producto: this.getProductoNombre(item.id_producto),
            sucursal: this.getSucursalNombre(item.id_sucursal),
            cantidad_actual: item.cantidad_actual,
            stock_minimo: stockMinimo,
            faltante: 0,
            severidad: 'proximo' as const
          };
        }

        return null;
      })
      .filter((item): item is ReplenishmentVm => item !== null)
      .sort((a, b) =>
        a.severidad === b.severidad ? b.faltante - a.faltante : a.severidad === 'critico' ? -1 : 1
      )
      .slice(0, 8);
  });

  protected readonly criticalProductsCount = computed(
    () => this.replenishmentAlerts().filter((item) => item.severidad === 'critico').length
  );

  protected readonly branchComparison = computed<BranchComparisonVm[]>(() => {
    return this.sucursales().map((sucursal) => {
      const ventas = this.ventas().filter((item) => {
        if (item.id_sucursal !== sucursal.id_sucursal || !item.fecha) {
          return false;
        }

        return new Date(item.fecha) >= this.getWindowStartDate(this.selectedWindowMonths());
      });

      const inventarios = this.inventarios().filter((item) => item.id_sucursal === sucursal.id_sucursal);
      const transferencias = this.transferencias().filter((item) => {
        const activeState = (item.estado ?? item.envio?.estado_envio ?? '').toUpperCase();
        return (
          (item.id_sucursal_origen === sucursal.id_sucursal ||
            item.id_sucursal_destino === sucursal.id_sucursal) &&
          !['RECIBIDA', 'CERRADA', 'CANCELADA'].some((state) => activeState.includes(state))
        );
      });

      return {
        id_sucursal: sucursal.id_sucursal,
        nombre: sucursal.nombre,
        ventas_total: ventas.reduce((acc, item) => acc + item.total, 0),
        stock_total: inventarios.reduce((acc, item) => acc + item.cantidad_actual, 0),
        productos_criticos: inventarios.filter(
          (item) =>
            this.getProductoStockMinimo(item.id_producto) > 0 &&
            item.cantidad_actual <= this.getProductoStockMinimo(item.id_producto)
        ).length,
        transferencias_activas: transferencias.length
      };
    });
  });

  protected readonly totalStock = computed(() =>
    this.inventariosFiltrados().reduce((acc, item) => acc + item.cantidad_actual, 0)
  );
  protected readonly inventoryTurnover = computed(() => {
    const demandTotal = this.demandByProduct().reduce((acc, item) => acc + item.cantidad, 0);
    const stock = this.totalStock();
    return stock ? demandTotal / stock : 0;
  });
  protected readonly activeTransferCount = computed(() => this.activeTransfers().length);
  protected readonly hasData = computed(
    () =>
      this.ventas().length > 0 ||
      this.inventarios().length > 0 ||
      this.transferencias().length > 0 ||
      this.compras().length > 0
  );

  constructor() {
    effect(() => {
      this.salesMonths();
      this.topDemandProducts();
      this.transferStateSummary();
      this.branchComparison();
      queueMicrotask(() => this.renderCharts());
    });
  }

  ngOnInit(): void {
    if (this.fixedSucursalId()) {
      this.filterForm.controls.id_sucursal.setValue(this.fixedSucursalId() ?? 0, {
        emitEvent: false
      });
    }

    this.cargarDashboard();
  }

  ngAfterViewInit(): void {
    this.renderCharts();
  }

  protected formatDelta(value: number): string {
    const prefix = value > 0 ? '+' : '';
    return `${prefix}${value.toFixed(1)}% vs periodo anterior`;
  }

  protected getSeverityLabel(severidad: 'critico' | 'proximo'): string {
    return severidad === 'critico' ? 'Critico' : 'Proximo al minimo';
  }

  protected getSeverityClass(severidad: 'critico' | 'proximo'): string {
    return severidad === 'critico' ? 'is-critical' : 'is-warning';
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

  protected getProductoNombre(idProducto: number | null | undefined): string {
    if (!idProducto) {
      return 'Sin producto';
    }

    return (
      this.productos().find((item) => item.id_producto === idProducto)?.nombre ??
      `Producto #${idProducto}`
    );
  }

  private getProductoStockMinimo(idProducto: number): number {
    return this.productos().find((item) => item.id_producto === idProducto)?.stock_minimo ?? 0;
  }

  private cargarDashboard(): void {
    this.loading.set(true);
    this.errorMessage.set('');

    forkJoin({
      ventasResponse: this.ventasApi.venta.listarVentas(),
      inventariosResponse: this.inventarioApi.inventarioSucursal.listarInventarioSucursal(),
      productosResponse: this.inventarioApi.productos.listarProductos(),
      sucursalesResponse: this.sucursalesApi.listarSucursales(),
      transferenciasResponse: this.transferenciasApi.transferencia.listarTransferencias(),
      comprasResponse: this.comprasApi.ordenesCompra.listarOrdenesCompra()
    })
      .pipe(
        switchMap((base) => {
          const ventas = this.extractData<VentaDto[]>(base.ventasResponse);
          const transferencias = this.extractData<TransferenciaDto[]>(base.transferenciasResponse);

          const ventaDetalles$ = ventas.length
            ? forkJoin(
                ventas.map((venta) =>
                  this.ventasApi.detallesVenta.listarDetallesPorVenta(venta.id_venta).pipe(
                    map((response) => ({
                      id: venta.id_venta,
                      detalles: this.extractData<DetalleVentaDto[]>(response)
                    }))
                  )
                )
              )
            : of([]);

          const transferenciaDetalles$ = transferencias.length
            ? forkJoin(
                transferencias.map((transferencia) =>
                  this.transferenciasApi.detallesTransferencia
                    .listarDetallesPorTransferencia(transferencia.id_transferencia)
                    .pipe(
                      map((response) => ({
                        id: transferencia.id_transferencia,
                        detalles: this.extractData<DetalleTransferenciaDto[]>(response)
                      }))
                    )
                )
              )
            : of([]);

          return forkJoin({
            ventaDetalles: ventaDetalles$,
            transferenciaDetalles: transferenciaDetalles$
          }).pipe(map((details) => ({ base, details })));
        }),
        finalize(() => this.loading.set(false)),
        takeUntilDestroyed(this.destroyRef)
      )
      .subscribe({
        next: ({ base, details }) => {
          this.ventas.set(this.extractData<VentaDto[]>(base.ventasResponse));
          this.inventarios.set(this.extractData<InventarioSucursalDto[]>(base.inventariosResponse));
          this.productos.set(this.extractData<ProductoDto[]>(base.productosResponse));
          this.sucursales.set(this.extractData<SucursalDto[]>(base.sucursalesResponse));
          this.transferencias.set(this.extractData<TransferenciaDto[]>(base.transferenciasResponse));
          this.compras.set(this.extractData<OrdenCompraDto[]>(base.comprasResponse));
          this.ventaDetallesMap.set(
            Object.fromEntries(details.ventaDetalles.map((item) => [item.id, item.detalles]))
          );
          this.transferenciaDetallesMap.set(
            Object.fromEntries(
              details.transferenciaDetalles.map((item) => [item.id, item.detalles])
            )
          );
          this.renderCharts();
        },
        error: () => {
          this.errorMessage.set('No se pudo cargar la informacion analitica del dashboard.');
        }
      });
  }

  private renderCharts(): void {
    this.renderSalesChart();
    this.renderDemandChart();
    this.renderTransferChart();
    this.renderBranchChart();
  }

  private renderSalesChart(): void {
    const canvas = this.salesChartRef?.nativeElement;
    if (!canvas) {
      return;
    }

    const labels = this.salesMonths().map((item) => item.label);
    const data = this.salesMonths().map((item) => item.total);

    if (!this.salesChart) {
      this.salesChart = new Chart(canvas, {
        type: 'line',
        data: {
          labels,
          datasets: [
            {
              label: 'Ventas',
              data,
              borderColor: '#0f766e',
              backgroundColor: 'rgba(15, 118, 110, 0.16)',
              pointBackgroundColor: '#0f766e',
              fill: true,
              tension: 0.35
            }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { display: false }
          }
        }
      });
      return;
    }

    this.salesChart.data.labels = labels;
    this.salesChart.data.datasets[0].data = data;
    this.salesChart.update();
  }

  private renderDemandChart(): void {
    const canvas = this.demandChartRef?.nativeElement;
    if (!canvas) {
      return;
    }

    const labels = this.topDemandProducts().map((item) => item.nombre);
    const data = this.topDemandProducts().map((item) => item.cantidad);

    if (!this.demandChart) {
      this.demandChart = new Chart(canvas, {
        type: 'bar',
        data: {
          labels,
          datasets: [
            {
              label: 'Unidades vendidas',
              data,
              backgroundColor: ['#0f766e', '#0d9488', '#14b8a6', '#7dd3fc', '#f59e0b']
            }
          ]
        },
        options: {
          indexAxis: 'y',
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { display: false }
          }
        }
      });
      return;
    }

    this.demandChart.data.labels = labels;
    this.demandChart.data.datasets[0].data = data;
    this.demandChart.update();
  }

  private renderTransferChart(): void {
    const canvas = this.transferChartRef?.nativeElement;
    if (!canvas) {
      return;
    }

    const labels = this.transferStateSummary().map((item) => item.estado);
    const data = this.transferStateSummary().map((item) => item.total);

    if (!this.transferChart) {
      this.transferChart = new Chart(canvas, {
        type: 'doughnut',
        data: {
          labels,
          datasets: [
            {
              label: 'Transferencias',
              data,
              backgroundColor: ['#0f766e', '#f59e0b', '#ef4444', '#3b82f6', '#8b5cf6', '#14b8a6']
            }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false
        }
      });
      return;
    }

    this.transferChart.data.labels = labels;
    this.transferChart.data.datasets[0].data = data;
    this.transferChart.update();
  }

  private renderBranchChart(): void {
    const canvas = this.branchChartRef?.nativeElement;
    if (!canvas || !this.canCompareBranches()) {
      return;
    }

    const labels = this.branchComparison().map((item) => item.nombre);
    const data = this.branchComparison().map((item) => item.ventas_total);

    if (!this.branchChart) {
      this.branchChart = new Chart(canvas, {
        type: 'bar',
        data: {
          labels,
          datasets: [
            {
              label: 'Ventas por sucursal',
              data,
              backgroundColor: '#1d4ed8'
            }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { display: false }
          }
        }
      });
      return;
    }

    this.branchChart.data.labels = labels;
    this.branchChart.data.datasets[0].data = data;
    this.branchChart.update();
  }

  private buildMonthBuckets(months: number): Array<{ key: string; label: string }> {
    const formatter = new Intl.DateTimeFormat('es-CO', { month: 'short', year: '2-digit' });
    const result: Array<{ key: string; label: string }> = [];
    const now = new Date();

    for (let offset = months - 1; offset >= 0; offset -= 1) {
      const date = new Date(now.getFullYear(), now.getMonth() - offset, 1);
      result.push({
        key: `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}`,
        label: formatter.format(date)
      });
    }

    return result;
  }

  private getWindowStartDate(months: number): Date {
    const now = new Date();
    return new Date(now.getFullYear(), now.getMonth() - (months - 1), 1);
  }

  private getTransferImpactLabel(item: TransferenciaDto, cantidad: number): string {
    const selectedSucursalId = this.selectedSucursalId();

    if (selectedSucursalId && item.id_sucursal_origen === selectedSucursalId) {
      return `Salida esperada de ${cantidad} und.`;
    }

    if (selectedSucursalId && item.id_sucursal_destino === selectedSucursalId) {
      return `Ingreso esperado de ${cantidad} und.`;
    }

    return `${cantidad} und. en movimiento`;
  }

  private extractData<T>(response: ApiResponseDto<T> | T): T {
    if (response && typeof response === 'object' && 'data' in response) {
      return response.data;
    }

    return response as T;
  }
}
