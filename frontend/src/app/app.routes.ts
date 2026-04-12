import { Routes } from '@angular/router';

import { authGuard } from './core/services/auth/guards/auth.guard';
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
        loadComponent: () =>
          import('./pages/dashboard/dashboard.page').then((module) => module.DashboardPage)
      },
      {
        path: 'operacion',
        loadComponent: () =>
          import('./pages/operacion/operacion.page').then((module) => module.OperacionPage)
      },
      {
        path: 'inventario',
        loadComponent: () =>
          import('./pages/inventario/inventario.page').then((module) => module.InventarioPage)
      },
      {
        path: 'compras',
        loadComponent: () =>
          import('./pages/compras/compras.page').then((module) => module.ComprasPage)
      },
      {
        path: 'ventas',
        loadComponent: () =>
          import('./pages/ventas/ventas.page').then((module) => module.VentasPage)
      },
      {
        path: 'transferencias',
        loadComponent: () =>
          import('./pages/transferencias/transferencias.page').then(
            (module) => module.TransferenciasPage
          )
      },
      {
        path: 'logistica',
        loadComponent: () =>
          import('./pages/logistica/logistica.page').then((module) => module.LogisticaPage)
      },
      {
        path: 'administracion',
        loadComponent: () =>
          import('./pages/administracion/administracion.page').then(
            (module) => module.AdministracionPage
          )
      },
      {
        path: 'reportes',
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
