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
    icon: 'dashboard',
    description: 'Resumen operativo y estado general',
    roles: [UserRoleDto.ADMIN_GENERAL, UserRoleDto.ADMIN_SUCURSAL],
    isDefaultFor: [UserRoleDto.ADMIN_GENERAL, UserRoleDto.ADMIN_SUCURSAL]
  },
  {
    label: 'Operacion',
    path: '/app/operacion',
    icon: 'inventario',
    description: 'Prioridades inmediatas de la sucursal',
    roles: [UserRoleDto.OPERARIO_INVENTARIO],
    isDefaultFor: [UserRoleDto.OPERARIO_INVENTARIO]
  },
  {
    label: 'Inventario',
    path: '/app/inventario',
    icon: 'inventario',
    description: 'Consulta existencias, alertas y movimientos operativos.',
    roles: [UserRoleDto.ADMIN_SUCURSAL, UserRoleDto.OPERARIO_INVENTARIO]
  },
  {
    label: 'Compras',
    path: '/app/compras',
    icon: 'compras',
    description: 'Ordenes, proveedores y abastecimiento',
    roles: [UserRoleDto.ADMIN_GENERAL, UserRoleDto.ADMIN_SUCURSAL, UserRoleDto.OPERARIO_INVENTARIO]
  },
  {
    label: 'Ventas',
    path: '/app/ventas',
    icon: 'ventas',
    description: 'Clientes, comprobantes y facturacion',
    roles: [UserRoleDto.ADMIN_GENERAL, UserRoleDto.ADMIN_SUCURSAL, UserRoleDto.OPERARIO_INVENTARIO]
  },
  {
    label: 'Transferencias',
    path: '/app/transferencias',
    icon: 'transferencias',
    description: 'Solicitudes, envios y recepciones',
    roles: [UserRoleDto.ADMIN_GENERAL, UserRoleDto.ADMIN_SUCURSAL, UserRoleDto.OPERARIO_INVENTARIO]
  },
  {
    label: 'Reportes',
    path: '/app/reportes',
    icon: 'reportes',
    description: 'Analitica y exportaciones',
    roles: [UserRoleDto.ADMIN_GENERAL, UserRoleDto.ADMIN_SUCURSAL]
  }
] as const;

function normalizeRole(role?: UserRoleDto | string | number | null): string | null {
  if (role === null || role === undefined) {
    return null;
  }

  const normalized = String(role).trim().toUpperCase();
  return normalized || null;
}

function includesRole(
  roles: readonly UserRoleDto[],
  role?: UserRoleDto | string | number | null
): boolean {
  const target = normalizeRole(role);

  if (!target) {
    return false;
  }

  return roles.some((item) => normalizeRole(item) === target);
}

export function getNavigationItemsByRole(role?: UserRoleDto | string | number | null): NavigationItem[] {
  if (!role) {
    return [];
  }

  return SECTION_ACCESS_CONFIG.filter((section) => includesRole(section.roles, role));
}

export function getAllowedRoutesByRole(role?: UserRoleDto | string | number | null): string[] {
  return getNavigationItemsByRole(role).map((section) => section.path);
}

export function getDefaultRouteByRole(role?: UserRoleDto | string | number | null): string {
  if (!role) {
    return '/app/operacion';
  }

  const defaultSection = SECTION_ACCESS_CONFIG.find((section) =>
    (section.isDefaultFor ?? []).some((item) => normalizeRole(item) === normalizeRole(role))
  );

  return defaultSection?.path ?? getNavigationItemsByRole(role)[0]?.path ?? '/app/operacion';
}