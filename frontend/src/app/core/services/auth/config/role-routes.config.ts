import { UserRoleDto } from '../dtos/user-role.dto';
import { getAllowedRoutesByRole } from '../../../config/section-access.config';

export const ROLE_ROUTES: Record<UserRoleDto, string[]> = {
  [UserRoleDto.ADMIN_GENERAL]: getAllowedRoutesByRole(UserRoleDto.ADMIN_GENERAL),
  [UserRoleDto.ADMIN_SUCURSAL]: getAllowedRoutesByRole(UserRoleDto.ADMIN_SUCURSAL),
  [UserRoleDto.OPERARIO_INVENTARIO]: getAllowedRoutesByRole(UserRoleDto.OPERARIO_INVENTARIO)
};
