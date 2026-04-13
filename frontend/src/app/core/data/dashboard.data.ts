import { ModuleSummary } from '../models/module-summary.model';

export const dashboardModules: ModuleSummary[] = [
  {
    title: 'Inventario',
    caption: 'Control de existencias',
    description: 'Base para productos, inventario por sucursal, ajustes y movimientos.'
  },
  {
    title: 'Compras',
    caption: 'Abastecimiento',
    description: 'Estructura inicial para ordenes de compra, proveedores y seguimiento.'
  },
  {
    title: 'Ventas',
    caption: 'Operacion comercial',
    description: 'Punto de partida para clientes, comprobantes, listas de precio y cobros.'
  },
  {
    title: 'Transferencias',
    caption: 'Logistica interna',
    description: 'Flujo base para solicitudes, despachos, recepciones e incidencias.'
  },
  {
    title: 'Reportes',
    caption: 'Indicadores y exportacion',
    description: 'Paneles resumidos para PDF, filtros por fechas y trazabilidad operativa.'
  },
  {
    title: 'Administracion',
    caption: 'Seguridad y parametros',
    description: 'Espacio reservado para roles, sesiones, catalogos y configuracion global.'
  }
];
