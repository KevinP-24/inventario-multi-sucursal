import { NavigationItem } from '../models/navigation-item.model';

export const navigationItems: NavigationItem[] = [
  {
    label: 'Dashboard',
    path: '/app/dashboard',
    icon: 'DB',
    description: 'Resumen operativo y estado general'
  },
  {
    label: 'Inventario',
    path: '/app/inventario',
    icon: 'IN',
    description: 'Productos, stock y movimientos'
  },
  {
    label: 'Compras',
    path: '/app/compras',
    icon: 'CO',
    description: 'Ordenes, proveedores y abastecimiento'
  },
  {
    label: 'Ventas',
    path: '/app/ventas',
    icon: 'VE',
    description: 'Clientes, comprobantes y facturacion'
  },
  {
    label: 'Transferencias',
    path: '/app/transferencias',
    icon: 'TR',
    description: 'Solicitudes, envios y recepciones'
  },
  {
    label: 'Reportes',
    path: '/app/reportes',
    icon: 'RP',
    description: 'Analitica y exportaciones'
  }
];
