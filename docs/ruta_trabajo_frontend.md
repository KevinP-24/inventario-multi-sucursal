# Ruta de trabajo frontend

## Decisión base

Vamos a usar una sola convención para contratos de datos:

- usar `dto`
- no mezclar `dto` y `model`

Esto nos deja una estructura más simple, consistente y fácil de defender.

## Dominios a reflejar

El frontend debe reflejar los dominios raíz del backend:

- `admin`
- `auth`
- `compras`
- `dashboard`
- `inventario`
- `logistica`
- `reportes`
- `sucursales`
- `transferencias`
- `ventas`

## Estructura esperada

```text
src/app/core/
  models/
    api-response.dto.ts
    paginated-response.dto.ts

  services/
    admin/
      admin-api.service.ts
      dtos/

    auth/
      auth-api.service.ts
      auth-session.service.ts
      guards/
      config/
      utils/
      dtos/

    compras/
      compras-api.service.ts
      dtos/

    dashboard/
      dashboard-api.service.ts
      dtos/

    inventario/
      inventario-api.service.ts
      dtos/

    logistica/
      logistica-api.service.ts
      dtos/

    reportes/
      reportes-api.service.ts
      dtos/

    sucursales/
      sucursales-api.service.ts
      dtos/

    transferencias/
      transferencias-api.service.ts
      dtos/

    ventas/
      ventas-api.service.ts
      dtos/
```

## Regla de implementación

Si existe un submódulo en backend, en frontend debe existir al menos:

1. un DTO dentro del dominio
2. un método en el `*-api.service.ts` del dominio

Ejemplo:

- si backend tiene `ventas/cliente`, frontend debe tener algo como `cliente.dto.ts`
- si backend expone un endpoint de clientes, ese método va en `ventas-api.service.ts`

## Qué va en cada dominio

### `dashboard`

Solo datos agregados:

- KPIs
- resúmenes
- alertas agregadas
- comparativas
- tarjetas y paneles

### `inventario`

Todo lo operativo:

- inventario por sucursal
- productos
- movimientos
- ajustes
- devoluciones
- mermas
- listas de precio
- precios por producto
- unidades

### `compras`

- órdenes de compra
- detalle
- recepción
- histórico
- proveedores

### `ventas`

- ventas
- detalle de venta
- clientes
- tipo de documento
- comprobantes

### `transferencias`

- transferencias
- detalle
- estados
- recepción
- incidencias

### `logistica`

- envíos
- rutas
- prioridades
- transportistas

### `reportes`

- PDF
- Excel
- filtros
- consolidados

### `auth`

- login
- sesión
- usuario
- rol

### `admin`

- parámetros del sistema

### `sucursales`

- sucursales

## Regla de servicios

No crear un servicio Angular por cada submódulo interno.

Sí crear:

- un `*-api.service.ts` por dominio raíz

Ejemplo:

- `inventario-api.service.ts` concentra endpoints de `inventario_sucursal`, `producto`, `movimiento_inventario`, `lista_precio`, `precio_producto`
- `ventas-api.service.ts` concentra endpoints de `venta`, `detalle_venta`, `cliente`, `tipo_documento`
- `transferencias-api.service.ts` concentra endpoints de `transferencia`, `detalle_transferencia`, `estado_transferencia`, `recepcion_transferencia`, `incidencia_transferencia`

## Regla de DTOs

Usar DTOs para todo:

- response de endpoint
- payload de creación
- payload de actualización
- filtros

Ejemplos:

```text
core/services/inventario/dtos/
  inventario-sucursal.dto.ts
  producto.dto.ts
  producto-unidad.dto.ts
  movimiento-inventario.dto.ts
  lista-precio.dto.ts
  precio-producto.dto.ts
  unidad-medida.dto.ts
  stock-alert.dto.ts
  crear-inventario-sucursal.dto.ts
  ajustar-inventario.dto.ts
```

```text
core/services/ventas/dtos/
  venta.dto.ts
  detalle-venta.dto.ts
  cliente.dto.ts
  tipo-documento.dto.ts
  crear-venta.dto.ts
```

```text
core/services/transferencias/dtos/
  transferencia.dto.ts
  detalle-transferencia.dto.ts
  estado-transferencia.dto.ts
  recepcion-transferencia.dto.ts
  incidencia-transferencia.dto.ts
  crear-transferencia.dto.ts
  revisar-transferencia.dto.ts
  registrar-envio-transferencia.dto.ts
  confirmar-recepcion-transferencia.dto.ts
```

## Páginas

Las páginas deben mantenerse limpias.

Recomendado:

```text
pages/dashboard/
  dashboard.page.ts
  dashboard.facade.ts

pages/operacion/operador/
  operacion.page.ts
  operacion.facade.ts
```

La `facade`:

- llama servicios
- junta respuestas
- adapta datos para UI

## Orden de implementación

1. `dashboard`
2. `inventario`
3. `transferencias`
4. `ventas`
5. `compras`
6. `reportes`
7. `logistica`
8. `admin`
9. `sucursales`

## Respuesta para sustentación

Si preguntan “¿dónde implementaría algo nuevo?”:

1. ubico el dominio en `backend/app/modules`
2. creo o ajusto el DTO en `core/services/<dominio>/dtos/`
3. agrego el método en `core/services/<dominio>/<dominio>-api.service.ts`
4. si es agregado de tablero, va en `dashboard`
5. si es exportación, va en `reportes`

## Decisión final

Se adopta esta convención:

- un servicio por dominio raíz
- un solo tipo de contrato: `dto`
- `dashboard` solo para resúmenes
- estructura espejo del backend

## Qué va en cada modulo

### `core/services/dashboard/`

Solo datos agregados y listos para pintar tablero:

- KPIs
- resumenes
- alertas agregadas
- comparativas
- tarjetas y paneles

Ejemplos de metodos:

- `getSalesSummary(branchId)`
- `getDemandSummary(branchId)`
- `getActiveTransfers(branchId)`
- `getRestockAlerts(branchId)`
- `getBranchPerformance()`

No debe contener:

- CRUD operativo de inventario
- registro de ventas
- gestion de ordenes de compra
- flujo transaccional de transferencias

### `core/services/inventario/`

Todo lo operativo del inventario:

- stock por sucursal
- detalle de inventario o producto en sucursal
- movimientos
- ingresos
- retiros
- devoluciones
- mermas
- alertas de stock si el endpoint pertenece realmente a inventario

Ejemplos de metodos:

- `listarInventario()`
- `obtenerInventario(idInventario)`
- `listarAlertasStockBajo(idSucursal)`
- `crearInventario(payload)`
- `actualizarInventario(idInventario, payload)`
- `ajustarInventario(idInventario, payload)`
- `registrarDevolucion(idInventario, payload)`
- `registrarMerma(idInventario, payload)`

### `core/services/compras/`

Todo el flujo de compras:

- ordenes de compra
- detalle
- recepcion
- historico

Ejemplos de metodos:

- `listarOrdenesCompra()`
- `obtenerOrdenCompra(idOrdenCompra)`
- `filtrarHistorialCompras(filtros)`
- `crearOrdenCompra(payload)`
- `anularOrdenCompra(idOrdenCompra)`
- `recibirOrdenCompra(idOrdenCompra, payload)`

### `core/services/ventas/`

Todo el flujo de ventas:

- registrar venta
- listar ventas
- detalle
- comprobantes

Ejemplos de metodos:

- `listarVentas()`
- `obtenerVenta(idVenta)`
- `crearVenta(payload)`

Si luego aparecen endpoints de historial, filtros o comprobantes, van aqui.

### `core/services/transferencias/`

Todo el flujo transaccional de transferencias:

- solicitar
- aprobar o rechazar
- enviar
- recibir
- incidencias
- estados

Ejemplos de metodos:

- `listarTransferencias()`
- `obtenerTransferencia(idTransferencia)`
- `crearTransferencia(payload)`
- `revisarTransferencia(idTransferencia, payload)`
- `registrarEnvioTransferencia(idTransferencia, payload)`
- `confirmarRecepcionTransferencia(idTransferencia, payload)`

### `core/services/reportes/`

Todo lo exportable o consolidado:

- PDF
- Excel
- filtros
- historicos consolidados

Ejemplos de metodos:

- `exportarVentasPdf(filtros)`
- `exportarInventarioPdf(filtros)`
- `exportarTransferenciasPdf(filtros)`

Si despues aparecen exportaciones Excel, van en este mismo modulo.

## Qué va en `core/models/`

Solo modelos globales compartidos:

- `ApiResponse<T>`
- `PaginatedResponse<T>`
- `SelectOption`
- `TableQueryParams`

No meter aqui modelos de negocio como:

- `Venta`
- `OrdenCompra`
- `Transferencia`
- `Inventario`

Esos pertenecen a su modulo.

## Cómo manejar modelos por dominio

Cada dominio debe tener sus modelos propios y, cuando crezcan, dividirse en archivos pequeños.

Ejemplo recomendado:

```text
core/services/inventario/models/
  inventario-item.model.ts
  movimiento-inventario.model.ts
  stock-alert.model.ts
  crear-inventario.payload.ts
  ajustar-inventario.payload.ts
```

Evitar:

- un archivo gigante con todos los tipos del dominio

Nota:

- mientras el modulo apenas nace, se puede arrancar con un `inventario.model.ts`
- cuando el dominio crezca, se divide por responsabilidad

## Convencion de nombres

Usar una sola convención y mantenerla:

- `inventario-api.service.ts`
- `compras-api.service.ts`
- `ventas-api.service.ts`
- `transferencias-api.service.ts`
- `reportes-api.service.ts`
- `dashboard-api.service.ts`

No mezclar variantes como:

- `inventario.service.ts`
- `inventario-http.service.ts`
- `inventario-api.service.ts`

## Cómo pensar el dashboard

Hay dos vistas claras:

### `DashboardPage`

Pensada para administrador general y administrador de sucursal:

- indicadores generales
- ventas
- estado global o local
- comparativas
- resumenes

Debe consumir principalmente:

- `DashboardApiService`

### `OperacionPage`

Pensada para operario:

- reabastecimiento
- transferencias activas
- referencias criticas
- foco operativo inmediato

Debe mostrar informacion accionable y resumida, no todo el dominio completo.

Tambien puede consumir:

- `DashboardApiService`

Porque alli viven las vistas agregadas y operativas del tablero.

## Qué NO hacer

No hacer esto:

```text
core/services/dashboard/
  dashboard-api.service.ts
  inventario-api.service.ts
  compras-api.service.ts
  ventas-api.service.ts
```

Eso mezcla dashboard con negocio y rompe la organizacion del proyecto.

## Qué hacer en los componentes

El componente no deberia hablar con muchos servicios directos si se puede evitar.

Buena opcion:

```text
pages/dashboard/
  dashboard.page.ts
  dashboard.page.html
  dashboard.page.css
  dashboard.facade.ts

pages/operacion/operador/
  operacion.page.ts
  operacion.page.html
  operacion.page.css
  operacion.facade.ts
```

## Qué hace una facade

La facade:

- llama varios servicios
- junta respuestas
- transforma datos para UI
- deja el componente limpio

Ejemplo:

```ts
import { Injectable, inject } from '@angular/core';
import { forkJoin } from 'rxjs';

import { DashboardApiService } from '../../../core/services/dashboard/dashboard-api.service';

@Injectable()
export class OperacionFacade {
  private readonly dashboardApi = inject(DashboardApiService);

  load(branchId: number | null) {
    return forkJoin({
      restockAlerts: this.dashboardApi.getRestockAlerts(branchId),
      activeTransfers: this.dashboardApi.getActiveTransfers(branchId),
      demandSummary: this.dashboardApi.getDemandSummary(branchId)
    });
  }
}
```

## Estado base actual del frontend

Ya existe o ya se dejo creado:

- `core/services/dashboard/dashboard-api.service.ts`
- `core/services/inventario/inventario-api.service.ts`
- `core/services/compras/compras-api.service.ts`
- `core/services/ventas/ventas-api.service.ts`
- `core/services/transferencias/transferencias-api.service.ts`
- `core/services/reportes/reportes-api.service.ts`
- `core/models/api-response.model.ts`
- `core/models/paginated-response.model.ts`

Pendiente de refinar:

- dividir modelos grandes por dominio en archivos mas pequeños
- crear `dashboard.facade.ts`
- crear `operacion.facade.ts`
- conectar paginas con sus servicios o facades

## Hoja de ruta recomendada

### Fase 1. Dashboard operativo

Objetivo:

dejar funcionales las vistas de tablero y operacion con datos reales.

Tareas:

- conectar `DashboardPage` a `DashboardApiService`
- crear `dashboard.facade.ts`
- crear `operacion.facade.ts`
- cargar:
  - resumen de ventas
  - rotacion y demanda
  - alertas de reabastecimiento
  - transferencias activas
  - comparativa entre sucursales

Modulos implicados:

- `dashboard`

### Fase 2. Inventario

Objetivo:

dejar lista la base operativa de inventario.

Tareas:

- definir modelos separados de inventario
- conectar pagina de inventario al `InventarioApiService`
- listar stock por sucursal
- mostrar alertas de stock bajo
- preparar acciones de ajuste, devolucion y merma

Modulos implicados:

- `inventario`

### Fase 3. Transferencias

Objetivo:

dejar visible el ciclo de transferencias en frontend.

Tareas:

- separar modelos de transferencia por responsabilidad
- listar transferencias
- mostrar detalle
- preparar flujo de revision, envio y recepcion
- decidir como mostrar incidencias y estados

Modulos implicados:

- `transferencias`

### Fase 4. Ventas

Objetivo:

conectar el flujo comercial principal.

Tareas:

- listar ventas
- mostrar detalle de venta
- preparar formulario de registro
- definir visualizacion de comprobante

Modulos implicados:

- `ventas`

### Fase 5. Compras

Objetivo:

cerrar abastecimiento desde frontend.

Tareas:

- listar ordenes de compra
- mostrar detalle
- filtrar historico
- preparar acciones de crear, anular y recibir

Modulos implicados:

- `compras`

### Fase 6. Reportes

Objetivo:

dejar exportaciones y consultas consolidadas.

Tareas:

- conectar exportacion PDF
- preparar exportacion Excel cuando exista endpoint
- definir filtros reutilizables

Modulos implicados:

- `reportes`

## Orden inmediato recomendado

Para avanzar con mayor rendimiento:

1. `dashboard`
2. `inventario`
3. `transferencias`
4. `ventas`
5. `compras`
6. `reportes`

La razon:

- `dashboard`, `inventario` y `transferencias` alimentan mas rapido la operacion real
- despues `ventas` y `compras` cierran el flujo de negocio
- `reportes` remata exportables y consolidados

## Decision de arquitectura

Mantener:

- `core/services/dashboard/dashboard-api.service.ts`

Crear y sostener como dominios separados:

- `core/services/inventario/inventario-api.service.ts`
- `core/services/compras/compras-api.service.ts`
- `core/services/ventas/ventas-api.service.ts`
- `core/services/transferencias/transferencias-api.service.ts`
- `core/services/reportes/reportes-api.service.ts`

No meter todo dentro de `dashboard`.

Ese criterio se mantiene para evitar que la carpeta se vuelva un contenedor mezclado de todo el negocio.
