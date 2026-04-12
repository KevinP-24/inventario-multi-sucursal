import { CommonModule } from '@angular/common';
import { HttpErrorResponse } from '@angular/common/http';
import {
  ChangeDetectionStrategy,
  Component,
  DestroyRef,
  computed,
  inject,
  signal
} from '@angular/core';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { finalize, forkJoin } from 'rxjs';

import { AdminApiService } from '../../core/services/admin/admin-api.service';
import {
  GuardarParametroSistemaDto,
  ParametroSistemaDto
} from '../../core/services/admin/dtos/parametro-sistema.dto';
import { AuthSessionService } from '../../core/services/auth/auth-session.service';
import { RoleDto } from '../../core/services/auth/dtos/role.dto';
import { SaveUserDto } from '../../core/services/auth/dtos/user.dto';
import { UserRoleDto } from '../../core/services/auth/dtos/user-role.dto';
import { AuthUserDto } from '../../core/services/auth/dtos/auth-user.dto';
import { RolesApiService } from '../../core/services/auth/roles-api.service';
import { UsuariosApiService } from '../../core/services/auth/usuarios-api.service';
import { ComprasApiService } from '../../core/services/compras/compras-api.service';
import { OrdenCompraDto } from '../../core/services/compras/dtos/orden-compra.dto';
import { InventarioApiService } from '../../core/services/inventario/inventario-api.service';
import { InventarioSucursalDto } from '../../core/services/inventario/dtos/inventario-sucursal.dto';
import { ProductoDto } from '../../core/services/inventario/dtos/producto.dto';
import { ApiResponseDto } from '../../core/models/api-response.dto';
import { ReportesApiService } from '../../core/services/reportes/reportes-api.service';
import { ReporteFiltrosDto } from '../../core/services/reportes/dtos/reporte-filtros.dto';
import {
  GuardarSucursalDto,
  SucursalDto
} from '../../core/services/sucursales/dtos/sucursal.dto';
import { SucursalesApiService } from '../../core/services/sucursales/sucursales-api.service';
import { TransferenciaDto } from '../../core/services/transferencias/dtos/transferencia.dto';
import { TransferenciasApiService } from '../../core/services/transferencias/transferencias-api.service';
import { VentaDto } from '../../core/services/ventas/dtos/venta.dto';
import { VentasApiService } from '../../core/services/ventas/ventas-api.service';
import { PageHeaderComponent } from '../../shared/components/page-header/page-header.component';

type AdministracionSection = 'usuarios' | 'sucursales' | 'parametros' | 'global';
type ReporteKind = 'inventario' | 'ventas' | 'transferencias';

interface SucursalGlobalVm {
  readonly id_sucursal: number;
  readonly nombre: string;
  readonly ciudad: string;
  readonly estado: string;
  readonly usuarios: number;
  readonly usuarios_activos: number;
  readonly productos_con_stock: number;
  readonly stock_total: number;
  readonly valor_inventario: number;
  readonly ventas: number;
  readonly total_ventas: number;
  readonly compras: number;
  readonly total_compras: number;
  readonly transferencias: number;
}

@Component({
  selector: 'app-administracion-page',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, PageHeaderComponent],
  templateUrl: './administracion.page.html',
  styleUrl: './administracion.page.css',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class AdministracionPage {
  private readonly fb = inject(FormBuilder);
  private readonly destroyRef = inject(DestroyRef);
  private readonly authSession = inject(AuthSessionService);
  private readonly usuariosApi = inject(UsuariosApiService);
  private readonly rolesApi = inject(RolesApiService);
  private readonly sucursalesApi = inject(SucursalesApiService);
  private readonly adminApi = inject(AdminApiService);
  private readonly inventarioApi = inject(InventarioApiService);
  private readonly comprasApi = inject(ComprasApiService);
  private readonly ventasApi = inject(VentasApiService);
  private readonly transferenciasApi = inject(TransferenciasApiService);
  private readonly reportesApi = inject(ReportesApiService);

  readonly currentUser = this.authSession.currentUser;
  readonly activeSection = signal<AdministracionSection>('usuarios');
  readonly loading = signal(false);
  readonly submittingUsuario = signal(false);
  readonly submittingSucursal = signal(false);
  readonly submittingParametro = signal(false);
  readonly downloadingReport = signal<ReporteKind | null>(null);
  readonly errorMessage = signal('');
  readonly successMessage = signal('');

  readonly usuarios = signal<AuthUserDto[]>([]);
  readonly roles = signal<RoleDto[]>([]);
  readonly sucursales = signal<SucursalDto[]>([]);
  readonly parametros = signal<ParametroSistemaDto[]>([]);
  readonly inventarios = signal<InventarioSucursalDto[]>([]);
  readonly productos = signal<ProductoDto[]>([]);
  readonly ordenesCompra = signal<OrdenCompraDto[]>([]);
  readonly ventas = signal<VentaDto[]>([]);
  readonly transferencias = signal<TransferenciaDto[]>([]);

  readonly selectedUsuarioId = signal<number | null>(null);
  readonly selectedSucursalId = signal<number | null>(null);
  readonly selectedParametroId = signal<number | null>(null);

  readonly usuarioForm = this.fb.nonNullable.group({
    nombre: ['', [Validators.required, Validators.maxLength(120)]],
    correo: ['', [Validators.required, Validators.email, Validators.maxLength(160)]],
    password: ['', [Validators.maxLength(160)]],
    id_rol: [0, [Validators.required, Validators.min(1)]],
    id_sucursal: [0],
    activo: [true]
  });

  readonly sucursalForm = this.fb.nonNullable.group({
    nombre: ['', [Validators.required, Validators.maxLength(120)]],
    direccion: ['', [Validators.required, Validators.maxLength(200)]],
    ciudad: ['', [Validators.required, Validators.maxLength(120)]],
    telefono: ['', [Validators.maxLength(40)]],
    estado: ['activa' as 'activa' | 'inactiva', [Validators.required]]
  });

  readonly parametroForm = this.fb.nonNullable.group({
    clave: ['', [Validators.required, Validators.maxLength(120)]],
    valor: ['', [Validators.required, Validators.maxLength(255)]],
    descripcion: ['', [Validators.maxLength(255)]],
    activo: [true]
  });

  readonly globalFiltersForm = this.fb.nonNullable.group({
    id_sucursal: [0],
    fecha_desde: [''],
    fecha_hasta: ['']
  });

  readonly rolesActivos = computed(() => this.roles().filter((item) => item.activo !== false));
  readonly sucursalesActivas = computed(() =>
    this.sucursales().filter((item) => item.estado?.toLowerCase?.() !== 'inactiva')
  );
  readonly usuariosActivos = computed(() => this.usuarios().filter((item) => item.activo));
  readonly parametrosActivos = computed(() => this.parametros().filter((item) => item.activo));

  readonly selectedRoleRequiresSucursal = computed(() => {
    const idRol = Number(this.usuarioForm.controls.id_rol.value || 0);
    const role = this.roles().find((item) => item.id_rol === idRol);
    return role?.codigo !== UserRoleDto.ADMIN_GENERAL;
  });

  readonly inventariosFiltrados = computed(() => {
    const idSucursal = Number(this.globalFiltersForm.controls.id_sucursal.value || 0);
    return this.inventarios().filter((item) => !idSucursal || item.id_sucursal === idSucursal);
  });

  readonly ventasFiltradas = computed(() => {
    const idSucursal = Number(this.globalFiltersForm.controls.id_sucursal.value || 0);
    const fechaDesde = this.globalFiltersForm.controls.fecha_desde.value;
    const fechaHasta = this.globalFiltersForm.controls.fecha_hasta.value;

    return this.ventas().filter((item) => {
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

  readonly comprasFiltradas = computed(() => {
    const idSucursal = Number(this.globalFiltersForm.controls.id_sucursal.value || 0);
    const fechaDesde = this.globalFiltersForm.controls.fecha_desde.value;
    const fechaHasta = this.globalFiltersForm.controls.fecha_hasta.value;

    return this.ordenesCompra().filter((item) => {
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

  readonly transferenciasFiltradas = computed(() => {
    const idSucursal = Number(this.globalFiltersForm.controls.id_sucursal.value || 0);
    const fechaDesde = this.globalFiltersForm.controls.fecha_desde.value;
    const fechaHasta = this.globalFiltersForm.controls.fecha_hasta.value;

    return this.transferencias().filter((item) => {
      if (
        idSucursal &&
        item.id_sucursal_origen !== idSucursal &&
        item.id_sucursal_destino !== idSucursal
      ) {
        return false;
      }

      if (fechaDesde && item.fecha_solicitud && item.fecha_solicitud.slice(0, 10) < fechaDesde) {
        return false;
      }

      if (fechaHasta && item.fecha_solicitud && item.fecha_solicitud.slice(0, 10) > fechaHasta) {
        return false;
      }

      return true;
    });
  });

  readonly totalUsuarios = computed(() => this.usuarios().length);
  readonly totalSucursales = computed(() => this.sucursales().length);
  readonly totalParametros = computed(() => this.parametros().length);
  readonly stockGlobal = computed(() =>
    this.inventariosFiltrados().reduce((acc, item) => acc + item.cantidad_actual, 0)
  );
  readonly valorInventarioGlobal = computed(() =>
    this.inventariosFiltrados().reduce(
      (acc, item) => acc + item.cantidad_actual * (item.costo_promedio ?? 0),
      0
    )
  );
  readonly totalVentasGlobal = computed(() =>
    this.ventasFiltradas().reduce((acc, item) => acc + item.total, 0)
  );
  readonly totalComprasGlobal = computed(() =>
    this.comprasFiltradas().reduce((acc, item) => acc + item.total, 0)
  );

  readonly sucursalGlobalVm = computed<SucursalGlobalVm[]>(() => {
    return this.sucursales().map((sucursal) => {
      const usuarios = this.usuarios().filter((item) => item.id_sucursal === sucursal.id_sucursal);
      const inventarios = this.inventariosFiltrados().filter(
        (item) => item.id_sucursal === sucursal.id_sucursal
      );
      const ventas = this.ventasFiltradas().filter(
        (item) => item.id_sucursal === sucursal.id_sucursal
      );
      const compras = this.comprasFiltradas().filter(
        (item) => item.id_sucursal === sucursal.id_sucursal
      );
      const transferencias = this.transferenciasFiltradas().filter(
        (item) =>
          item.id_sucursal_origen === sucursal.id_sucursal ||
          item.id_sucursal_destino === sucursal.id_sucursal
      );

      return {
        id_sucursal: sucursal.id_sucursal,
        nombre: sucursal.nombre,
        ciudad: sucursal.ciudad,
        estado: sucursal.estado,
        usuarios: usuarios.length,
        usuarios_activos: usuarios.filter((item) => item.activo).length,
        productos_con_stock: inventarios.filter((item) => item.cantidad_actual > 0).length,
        stock_total: inventarios.reduce((acc, item) => acc + item.cantidad_actual, 0),
        valor_inventario: inventarios.reduce(
          (acc, item) => acc + item.cantidad_actual * (item.costo_promedio ?? 0),
          0
        ),
        ventas: ventas.length,
        total_ventas: ventas.reduce((acc, item) => acc + item.total, 0),
        compras: compras.length,
        total_compras: compras.reduce((acc, item) => acc + item.total, 0),
        transferencias: transferencias.length
      };
    });
  });

  constructor() {
    this.cargarVista();
  }

  seleccionarSeccion(section: AdministracionSection): void {
    this.activeSection.set(section);
    this.errorMessage.set('');
    this.successMessage.set('');
  }

  cargarVista(): void {
    this.loading.set(true);
    this.errorMessage.set('');

    forkJoin({
      usuariosResponse: this.usuariosApi.listarUsuarios(),
      rolesResponse: this.rolesApi.listarRoles(),
      sucursalesResponse: this.sucursalesApi.listarSucursales(),
      parametrosResponse: this.adminApi.listarParametrosSistema(),
      inventariosResponse: this.inventarioApi.inventarioSucursal.listarInventarioSucursal(),
      productosResponse: this.inventarioApi.productos.listarProductos(),
      comprasResponse: this.comprasApi.ordenesCompra.listarOrdenesCompra(),
      ventasResponse: this.ventasApi.venta.listarVentas(),
      transferenciasResponse: this.transferenciasApi.transferencia.listarTransferencias()
    })
      .pipe(
        finalize(() => this.loading.set(false)),
        takeUntilDestroyed(this.destroyRef)
      )
      .subscribe({
        next: ({
          usuariosResponse,
          rolesResponse,
          sucursalesResponse,
          parametrosResponse,
          inventariosResponse,
          productosResponse,
          comprasResponse,
          ventasResponse,
          transferenciasResponse
        }) => {
          this.usuarios.set(this.extractData<AuthUserDto[]>(usuariosResponse));
          this.roles.set(this.extractData<RoleDto[]>(rolesResponse));
          this.sucursales.set(this.extractData<SucursalDto[]>(sucursalesResponse));
          this.parametros.set(this.extractData<ParametroSistemaDto[]>(parametrosResponse));
          this.inventarios.set(this.extractData<InventarioSucursalDto[]>(inventariosResponse));
          this.productos.set(this.extractData<ProductoDto[]>(productosResponse));
          this.ordenesCompra.set(this.extractData<OrdenCompraDto[]>(comprasResponse));
          this.ventas.set(this.extractData<VentaDto[]>(ventasResponse));
          this.transferencias.set(this.extractData<TransferenciaDto[]>(transferenciasResponse));
          this.ensureDefaults();
        },
        error: (error: HttpErrorResponse) => {
          this.errorMessage.set(
            this.resolveApiError(error, 'No se pudo cargar el modulo administrativo.')
          );
        }
      });
  }

  guardarUsuario(): void {
    if (this.usuarioForm.invalid) {
      this.usuarioForm.markAllAsTouched();
      return;
    }

    const value = this.usuarioForm.getRawValue();
    const payload: SaveUserDto = {
      nombre: value.nombre.trim(),
      correo: value.correo.trim().toLowerCase(),
      id_rol: Number(value.id_rol),
      id_sucursal: this.selectedRoleRequiresSucursal()
        ? Number(value.id_sucursal || 0) || null
        : null,
      activo: value.activo,
      password: value.password.trim() || undefined
    };

    if (!payload.id_sucursal && this.selectedRoleRequiresSucursal()) {
      this.errorMessage.set('Selecciona la sucursal asociada al usuario.');
      return;
    }

    if (!this.selectedUsuarioId() && !payload.password) {
      this.errorMessage.set('Define una contrasena para crear el usuario.');
      return;
    }

    this.submittingUsuario.set(true);
    this.errorMessage.set('');
    this.successMessage.set('');

    const request = this.selectedUsuarioId()
      ? this.usuariosApi.actualizarUsuario(this.selectedUsuarioId()!, payload)
      : this.usuariosApi.crearUsuario(payload);

    request
      .pipe(
        finalize(() => this.submittingUsuario.set(false)),
        takeUntilDestroyed(this.destroyRef)
      )
      .subscribe({
        next: () => {
          this.successMessage.set(
            this.selectedUsuarioId()
              ? 'Usuario actualizado correctamente.'
              : 'Usuario creado correctamente.'
          );
          this.resetUsuarioForm();
          this.cargarVista();
        },
        error: (error: HttpErrorResponse) => {
          this.errorMessage.set(this.resolveApiError(error, 'No se pudo guardar el usuario.'));
        }
      });
  }

  editarUsuario(usuario: AuthUserDto): void {
    this.activeSection.set('usuarios');
    this.selectedUsuarioId.set(usuario.id_usuario);
    this.usuarioForm.setValue({
      nombre: usuario.nombre,
      correo: usuario.correo,
      password: '',
      id_rol: usuario.id_rol,
      id_sucursal: usuario.id_sucursal ?? 0,
      activo: usuario.activo
    });
  }

  toggleEstadoUsuario(usuario: AuthUserDto): void {
    const payload: SaveUserDto = {
      nombre: usuario.nombre,
      correo: usuario.correo,
      id_rol: usuario.id_rol,
      id_sucursal: usuario.id_sucursal,
      activo: !usuario.activo
    };

    this.usuariosApi
      .actualizarUsuario(usuario.id_usuario, payload)
      .pipe(takeUntilDestroyed(this.destroyRef))
      .subscribe({
        next: () => {
          this.successMessage.set(
            payload.activo ? 'Usuario activado correctamente.' : 'Usuario desactivado correctamente.'
          );
          if (this.selectedUsuarioId() === usuario.id_usuario) {
            this.resetUsuarioForm();
          }
          this.cargarVista();
        },
        error: (error: HttpErrorResponse) => {
          this.errorMessage.set(this.resolveApiError(error, 'No se pudo actualizar el usuario.'));
        }
      });
  }

  guardarSucursal(): void {
    if (this.sucursalForm.invalid) {
      this.sucursalForm.markAllAsTouched();
      return;
    }

    this.submittingSucursal.set(true);
    this.errorMessage.set('');
    this.successMessage.set('');

    const value = this.sucursalForm.getRawValue();
    const payload: GuardarSucursalDto = {
      nombre: value.nombre.trim(),
      direccion: value.direccion.trim(),
      ciudad: value.ciudad.trim(),
      telefono: value.telefono.trim() || null,
      estado: value.estado
    };

    const request = this.selectedSucursalId()
      ? this.sucursalesApi.actualizarSucursal(this.selectedSucursalId()!, payload)
      : this.sucursalesApi.crearSucursal(payload);

    request
      .pipe(
        finalize(() => this.submittingSucursal.set(false)),
        takeUntilDestroyed(this.destroyRef)
      )
      .subscribe({
        next: () => {
          this.successMessage.set(
            this.selectedSucursalId()
              ? 'Sucursal actualizada correctamente.'
              : 'Sucursal creada correctamente.'
          );
          this.resetSucursalForm();
          this.cargarVista();
        },
        error: (error: HttpErrorResponse) => {
          this.errorMessage.set(this.resolveApiError(error, 'No se pudo guardar la sucursal.'));
        }
      });
  }

  editarSucursal(sucursal: SucursalDto): void {
    this.activeSection.set('sucursales');
    this.selectedSucursalId.set(sucursal.id_sucursal);
    this.sucursalForm.setValue({
      nombre: sucursal.nombre,
      direccion: sucursal.direccion,
      ciudad: sucursal.ciudad,
      telefono: sucursal.telefono ?? '',
      estado: sucursal.estado?.toLowerCase?.() === 'inactiva' ? 'inactiva' : 'activa'
    });
  }

  toggleEstadoSucursal(sucursal: SucursalDto): void {
    const nextEstado = sucursal.estado?.toLowerCase?.() === 'inactiva' ? 'activa' : 'inactiva';
    const payload: GuardarSucursalDto = {
      nombre: sucursal.nombre,
      direccion: sucursal.direccion,
      ciudad: sucursal.ciudad,
      telefono: sucursal.telefono,
      estado: nextEstado
    };

    this.sucursalesApi
      .actualizarSucursal(sucursal.id_sucursal, payload)
      .pipe(takeUntilDestroyed(this.destroyRef))
      .subscribe({
        next: () => {
          this.successMessage.set(
            nextEstado === 'activa'
              ? 'Sucursal activada correctamente.'
              : 'Sucursal desactivada correctamente.'
          );
          if (this.selectedSucursalId() === sucursal.id_sucursal) {
            this.resetSucursalForm();
          }
          this.cargarVista();
        },
        error: (error: HttpErrorResponse) => {
          this.errorMessage.set(this.resolveApiError(error, 'No se pudo actualizar la sucursal.'));
        }
      });
  }

  guardarParametro(): void {
    if (this.parametroForm.invalid) {
      this.parametroForm.markAllAsTouched();
      return;
    }

    this.submittingParametro.set(true);
    this.errorMessage.set('');
    this.successMessage.set('');

    const value = this.parametroForm.getRawValue();
    const payload: GuardarParametroSistemaDto = {
      clave: value.clave.trim(),
      valor: value.valor.trim(),
      descripcion: value.descripcion.trim() || null,
      activo: value.activo
    };

    const request = this.selectedParametroId()
      ? this.adminApi.actualizarParametroSistema(this.selectedParametroId()!, payload)
      : this.adminApi.crearParametroSistema(payload);

    request
      .pipe(
        finalize(() => this.submittingParametro.set(false)),
        takeUntilDestroyed(this.destroyRef)
      )
      .subscribe({
        next: () => {
          this.successMessage.set(
            this.selectedParametroId()
              ? 'Parametro actualizado correctamente.'
              : 'Parametro creado correctamente.'
          );
          this.resetParametroForm();
          this.cargarVista();
        },
        error: (error: HttpErrorResponse) => {
          this.errorMessage.set(this.resolveApiError(error, 'No se pudo guardar el parametro.'));
        }
      });
  }

  editarParametro(parametro: ParametroSistemaDto): void {
    this.activeSection.set('parametros');
    this.selectedParametroId.set(parametro.id_parametro);
    this.parametroForm.setValue({
      clave: parametro.clave,
      valor: parametro.valor,
      descripcion: parametro.descripcion ?? '',
      activo: parametro.activo
    });
  }

  toggleEstadoParametro(parametro: ParametroSistemaDto): void {
    const payload: GuardarParametroSistemaDto = {
      clave: parametro.clave,
      valor: parametro.valor,
      descripcion: parametro.descripcion,
      activo: !parametro.activo
    };

    this.adminApi
      .actualizarParametroSistema(parametro.id_parametro, payload)
      .pipe(takeUntilDestroyed(this.destroyRef))
      .subscribe({
        next: () => {
          this.successMessage.set(
            payload.activo
              ? 'Parametro activado correctamente.'
              : 'Parametro desactivado correctamente.'
          );
          if (this.selectedParametroId() === parametro.id_parametro) {
            this.resetParametroForm();
          }
          this.cargarVista();
        },
        error: (error: HttpErrorResponse) => {
          this.errorMessage.set(this.resolveApiError(error, 'No se pudo actualizar el parametro.'));
        }
      });
  }

  descargarReporte(kind: ReporteKind): void {
    const filtros = this.buildReporteFiltros();
    const request =
      kind === 'inventario'
        ? this.reportesApi.exportarInventarioPdf(filtros)
        : kind === 'ventas'
          ? this.reportesApi.exportarVentasPdf(filtros)
          : this.reportesApi.exportarTransferenciasPdf(filtros);

    this.downloadingReport.set(kind);
    this.errorMessage.set('');
    this.successMessage.set('');

    request
      .pipe(
        finalize(() => this.downloadingReport.set(null)),
        takeUntilDestroyed(this.destroyRef)
      )
      .subscribe({
        next: (blob) => {
          const nombre = `reporte-${kind}-${new Date().toISOString().slice(0, 10)}.pdf`;
          this.downloadBlob(blob, nombre);
          this.successMessage.set('Reporte generado correctamente.');
        },
        error: (error: HttpErrorResponse) => {
          this.errorMessage.set(this.resolveApiError(error, 'No se pudo generar el reporte.'));
        }
      });
  }

  resetUsuarioForm(): void {
    this.selectedUsuarioId.set(null);
    this.usuarioForm.reset({
      nombre: '',
      correo: '',
      password: '',
      id_rol: this.rolesActivos()[0]?.id_rol ?? 0,
      id_sucursal: 0,
      activo: true
    });
  }

  resetSucursalForm(): void {
    this.selectedSucursalId.set(null);
    this.sucursalForm.reset({
      nombre: '',
      direccion: '',
      ciudad: '',
      telefono: '',
      estado: 'activa'
    });
  }

  resetParametroForm(): void {
    this.selectedParametroId.set(null);
    this.parametroForm.reset({
      clave: '',
      valor: '',
      descripcion: '',
      activo: true
    });
  }

  protected getRolNombre(idRol: number | null | undefined): string {
    if (!idRol) {
      return 'Sin rol';
    }

    return this.roles().find((item) => item.id_rol === idRol)?.nombre ?? `Rol #${idRol}`;
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

  protected getEstadoSucursalClass(estado: string | null | undefined): string {
    return estado?.toLowerCase?.() === 'inactiva' ? 'is-inactive' : 'is-active';
  }

  protected getStateLabel(value: boolean): string {
    return value ? 'Activo' : 'Inactivo';
  }

  private ensureDefaults(): void {
    if (!this.usuarioForm.controls.id_rol.value && this.rolesActivos().length) {
      this.usuarioForm.controls.id_rol.setValue(this.rolesActivos()[0].id_rol);
    }
  }

  private buildReporteFiltros(): ReporteFiltrosDto {
    const idSucursal = Number(this.globalFiltersForm.controls.id_sucursal.value || 0);
    return {
      id_sucursal: idSucursal || undefined,
      fecha_desde: this.globalFiltersForm.controls.fecha_desde.value || undefined,
      fecha_hasta: this.globalFiltersForm.controls.fecha_hasta.value || undefined
    };
  }

  private downloadBlob(blob: Blob, filename: string): void {
    const url = URL.createObjectURL(blob);
    const anchor = document.createElement('a');
    anchor.href = url;
    anchor.download = filename;
    anchor.click();
    URL.revokeObjectURL(url);
  }

  private extractData<T>(response: ApiResponseDto<T> | T): T {
    if (response && typeof response === 'object' && 'data' in response) {
      return response.data;
    }

    return response as T;
  }

  private resolveApiError(error: HttpErrorResponse, fallback: string): string {
    const apiError = error.error as
      | {
          message?: string;
          errors?: Record<string, string | readonly string[]>;
        }
      | null;

    const detailErrors = apiError?.errors
      ? Object.values(apiError.errors)
          .flatMap((item) => (Array.isArray(item) ? item : [item]))
          .join(' ')
      : '';

    return [detailErrors, apiError?.message, fallback].find(
      (item) => typeof item === 'string' && item.trim() !== ''
    ) as string;
  }
}
