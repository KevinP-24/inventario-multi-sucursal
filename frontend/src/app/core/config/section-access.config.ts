import { NavigationItem } from '../models/navigation-item.model';
import { UserRoleDto } from '../services/auth/dtos/user-role.dto';

export interface SectionAccessConfig extends NavigationItem {
  readonly roles: readonly UserRoleDto[];
  readonly isDefaultFor?: readonly UserRoleDto[];
}

export const SECTION_ACCESS_CONFIG: readonly SectionAccessConfig[] = [
  {
    label: 'Dashboard',
    path: '/app/dashboard',
    icon: 'DB',
    description: 'Resumen operativo y estado general',
    roles: [UserRoleDto.ADMIN_GENERAL, UserRoleDto.ADMIN_SUCURSAL],
    isDefaultFor: [UserRoleDto.ADMIN_GENERAL, UserRoleDto.ADMIN_SUCURSAL]
  },
  {
    label: 'Operacion',
    path: '/app/operacion',
    icon: 'OP',
    description: 'Prioridades inmediatas de la sucursal',
    roles: [UserRoleDto.OPERARIO_INVENTARIO],
    isDefaultFor: [UserRoleDto.OPERARIO_INVENTARIO]
  },
  {
    label: 'Inventario',
    path: '/app/inventario',
    icon: 'IN',
    description: 'Productos, stock y movimientos',
    roles: [UserRoleDto.ADMIN_GENERAL, UserRoleDto.ADMIN_SUCURSAL, UserRoleDto.OPERARIO_INVENTARIO]
  },
  {
    label: 'Compras',
    path: '/app/compras',
    icon: 'CO',
    description: 'Ordenes, proveedores y abastecimiento',
    roles: [UserRoleDto.ADMIN_GENERAL, UserRoleDto.ADMIN_SUCURSAL, UserRoleDto.OPERARIO_INVENTARIO]
  },
  {
    label: 'Ventas',
    path: '/app/ventas',
    icon: 'VE',
    description: 'Clientes, comprobantes y facturacion',
    roles: [UserRoleDto.ADMIN_GENERAL, UserRoleDto.ADMIN_SUCURSAL, UserRoleDto.OPERARIO_INVENTARIO]
  },
  {
    label: 'Transferencias',
    path: '/app/transferencias',
    icon: 'TR',
    description: 'Solicitudes, envios y recepciones',
    roles: [UserRoleDto.ADMIN_GENERAL, UserRoleDto.ADMIN_SUCURSAL, UserRoleDto.OPERARIO_INVENTARIO]
  },
  {
    label: 'Reportes',
    path: '/app/reportes',
    icon: 'RP',
    description: 'Analitica y exportaciones',
    roles: [UserRoleDto.ADMIN_GENERAL, UserRoleDto.ADMIN_SUCURSAL]
  }
] as const;

export function getNavigationItemsByRole(role?: UserRoleDto | null): NavigationItem[] {
  if (!role) {
    return [];
  }

  return SECTION_ACCESS_CONFIG.filter((section) => section.roles.includes(role));
}

export function getAllowedRoutesByRole(role?: UserRoleDto | null): string[] {
  return getNavigationItemsByRole(role).map((section) => section.path);
}

export function getDefaultRouteByRole(role?: UserRoleDto | null): string {
  if (!role) {
    return '/app/operacion';
  }

  const defaultSection = SECTION_ACCESS_CONFIG.find((section) => section.isDefaultFor?.includes(role));

  return defaultSection?.path ?? getNavigationItemsByRole(role)[0]?.path ?? '/app/operacion';
}
