import { Routes } from '@angular/router';

import { authGuard } from './core/services/auth/guards/auth.guard';
import { roleGuard } from './core/services/auth/guards/role.guard';
import { UserRoleDto } from './core/services/auth/dtos/user-role.dto';
import { MainLayoutComponent } from './layout/main-layout/main-layout.component';

export const routes: Routes = [
  {
    path: '',
    pathMatch: 'full',
    redirectTo: 'login'
  },
  {
    path: 'login',
    loadComponent: () =>
      import('./pages/auth/login/login.page').then((module) => module.LoginPage)
  },
  {
    path: 'app',
    component: MainLayoutComponent,
    canActivate: [authGuard],
    children: [
      {
        path: '',
        pathMatch: 'full',
        redirectTo: 'dashboard'
      },
      {
        path: 'dashboard',
        canActivate: [roleGuard([UserRoleDto.ADMIN_GENERAL, UserRoleDto.ADMIN_SUCURSAL])],
        loadComponent: () =>
          import('./pages/dashboard/dashboard.page').then((module) => module.DashboardPage)
      },
      {
        path: 'operacion',
        canActivate: [roleGuard([UserRoleDto.OPERARIO_INVENTARIO])],
        loadComponent: () =>
          import('./pages/operacion/operacion.page').then((module) => module.OperacionPage)
      },
      {
        path: 'inventario',
        canActivate: [
          roleGuard([
            UserRoleDto.ADMIN_GENERAL,
            UserRoleDto.ADMIN_SUCURSAL,
            UserRoleDto.OPERARIO_INVENTARIO
          ])
        ],
        loadComponent: () =>
          import('./pages/inventario/inventario.page').then((module) => module.InventarioPage)
      },
      {
        path: 'compras',
        canActivate: [roleGuard([UserRoleDto.ADMIN_SUCURSAL])],
        loadComponent: () =>
          import('./pages/compras/compras.page').then((module) => module.ComprasPage)
      },
      {
        path: 'ventas',
        canActivate: [roleGuard([UserRoleDto.OPERARIO_INVENTARIO])],
        loadComponent: () =>
          import('./pages/ventas/ventas.page').then((module) => module.VentasPage)
      },
      {
        path: 'transferencias',
        canActivate: [
          roleGuard([
            UserRoleDto.ADMIN_GENERAL,
            UserRoleDto.ADMIN_SUCURSAL,
            UserRoleDto.OPERARIO_INVENTARIO
          ])
        ],
        loadComponent: () =>
          import('./pages/transferencias/transferencias.page').then(
            (module) => module.TransferenciasPage
          )
      },
      {
        path: 'logistica',
        canActivate: [roleGuard([UserRoleDto.ADMIN_GENERAL, UserRoleDto.ADMIN_SUCURSAL])],
        loadComponent: () =>
          import('./pages/logistica/logistica.page').then((module) => module.LogisticaPage)
      },
      {
        path: 'administracion',
        canActivate: [roleGuard([UserRoleDto.ADMIN_GENERAL])],
        loadComponent: () =>
          import('./pages/administracion/administracion.page').then(
            (module) => module.AdministracionPage
          )
      },
      {
        path: 'reportes',
        canActivate: [roleGuard([UserRoleDto.ADMIN_GENERAL, UserRoleDto.ADMIN_SUCURSAL])],
        loadComponent: () =>
          import('./pages/reportes/reportes.page').then((module) => module.ReportesPage)
      }
    ]
  },
  {
    path: '**',
    redirectTo: 'login'
  }
];
