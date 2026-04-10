# Ruta de trabajo backend

## Base revisada

Documentos revisados en `docs`:

- `Prueba Tecnica Inventario.pdf`
- `Levantamiento de Requerimientos.pdf`
- `Actores del sistema.pdf`
- `Diagrama de actividades.pdf`
- `Diagrama de arquitectura.pdf`
- `Diagrama entidad relacion_final.pdf`

El alcance funcional documentado se resume en estos bloques:

- Inventario: RF01-RF09
- Compras: RF10-RF16
- Ventas: RF17-RF22
- Transferencias: RF23-RF32
- Logistica: RF33-RF36
- Dashboard/analisis: RF37-RF40
- Administracion: RF41-RF44
- Reportes exportables: RF45-RF46

Actores documentados:

- Administrador general
- Gerente de sucursal
- Operador de inventario
- Sistema externo opcional, fuera del alcance base

Flujos obligatorios del diagrama de actividades:

- Flujo de venta
- Flujo de transferencia entre sucursales

## Estado actual del backend

### Implementado o avanzado

- Infraestructura Flask, PostgreSQL, Docker Compose y migraciones Alembic.
- Patron por modulo con `model`, `repository`, `schema`, `service` y `routes`.
- Base de actores: `rol`, `usuario`.
- Base administrativa: `sucursal`, `parametro_sistema`.
- Base comercial: `cliente`, `proveedor`.
- Inventario base: `producto`, `unidad_medida`, `producto_unidad`.
- Inventario por sede: `inventario_sucursal`.
- Trazabilidad: `tipo_movimiento_inventario`, `movimiento_inventario`.
- Precios: `lista_precio`, `precio_producto`.
- Logistica base: `transportista`, `ruta_logistica`.
- Compras base: `orden_compra`, `detalle_orden_compra`.
- Accion de recepcion de compra:
  `POST /api/v1/ordenes-compra/recibir_orden_compra/<id_orden_compra>`.

### Parcial

- RF08-RF09: historial y trazabilidad existen; falta robustecer filtros por rango, sucursal, producto y origen.
- RF10-RF14: compras ya cubren creacion, condiciones, recepcion y actualizacion de inventario.
- RF21: listas de precio y precio por producto existen como catalogos.
- RF33-RF36: rutas y transportistas existen como catalogos, pero falta el flujo de envio.
- RF41-RF43: usuarios, sucursales y parametros existen como CRUD basico.

### Faltante principal

- Autenticacion real con login JWT y proteccion de endpoints.
- Autorizacion por roles aplicada a rutas.
- Dashboard/KPIs.
- Reportes exportables PDF o Excel.
- Tests de flujos criticos.

## Ruta recomendada

### Fase 1. Cerrar compras e inventario operativo

Objetivo: dejar un primer flujo transaccional completo y defendible.

Tareas:

- Ajustar recepcion de orden de compra para calcular costo promedio ponderado.
- Crear endpoint de ajustes de inventario:
  entradas, salidas y ajuste manual con impacto en `inventario_sucursal`.
- Agregar filtros a movimientos:
  por sucursal, producto, tipo, modulo_origen, id_origen y rango de fechas.
- Definir respuesta de alerta de bajo stock comparando `cantidad_actual` contra `stock_minimo`.

Estado actual:

- Implementado costo promedio ponderado al recibir ordenes de compra.
- Implementado ajuste operativo de inventario:
  `POST /api/v1/inventario-sucursal/ajustar_inventario_sucursal/<id_inventario>`.
- Implementado filtro de movimientos:
  `GET /api/v1/movimientos-inventario/filtrar_movimientos_inventario`.
- Implementada alerta de stock bajo:
  `GET /api/v1/inventario-sucursal/listar_alertas_stock_bajo`.
- Implementada baja logica de producto:
  `DELETE /api/v1/productos/eliminar_producto/<id_producto>`.
- Implementada devolucion de inventario:
  `POST /api/v1/inventario-sucursal/registrar_devolucion_inventario/<id_inventario>`.
- Implementada merma de inventario:
  `POST /api/v1/inventario-sucursal/registrar_merma_inventario/<id_inventario>`.

RF cubiertos al cerrar la fase:

- RF01
- RF04
- RF05
- RF06 parcial
- RF08
- RF09
- RF13
- RF14
- RF16

### Fase 2. Implementar ventas

Objetivo: cubrir el flujo obligatorio de venta del diagrama de actividades.

Tareas:

- Crear migracion y modelos `venta` y `detalle_venta` segun DER final.
- Registrar venta con detalles en una sola transaccion.
- Validar stock antes de confirmar.
- Tomar precio desde `precio_producto` y `lista_precio`, permitiendo descuento.
- Descontar inventario.
- Crear movimientos tipo `SALIDA` con:
  `modulo_origen = "VENTA"` e `id_origen = id_venta`.
- Generar campo `comprobante`.
- Exponer endpoints de crear, listar, obtener y consultar historial de ventas.

Estado actual:

- Implementadas tablas `venta` y `detalle_venta` mediante migracion `012`.
- Implementado endpoint principal del flujo:
  `POST /api/v1/ventas/crear_venta`.
- Implementadas consultas:
  `GET /api/v1/ventas/listar_ventas`,
  `GET /api/v1/ventas/obtener_venta/<id_venta>` y
  `GET /api/v1/detalles-venta/listar_detalles_por_venta/<id_venta>`.
- La venta valida stock antes de confirmar, toma precios desde la lista de precios,
  permite descuento por detalle, descuenta inventario, genera comprobante y crea
  movimientos `SALIDA` con `modulo_origen = "VENTA"`.

RF cubiertos:

- RF17
- RF18
- RF19
- RF20
- RF21
- RF22
- RB03

### Fase 3. Implementar transferencias

Objetivo: cubrir el flujo obligatorio de transferencia entre sucursales.

Tareas:

- Crear migracion y modelos:
  `transferencia`, `detalle_transferencia`, `envio_transferencia`,
  `recepcion_transferencia`, `incidencia_transferencia`.
- Registrar solicitud desde sucursal destino u administrador.
- Revisar solicitud desde sucursal origen.
- Aprobar o ajustar cantidades segun disponibilidad.
- Registrar envio con ruta, transportista y fechas.
- Confirmar recepcion completa o parcial.
- En recepcion completa: descontar origen, sumar destino y crear movimientos.
- En recepcion parcial: registrar cantidades recibidas, faltantes e incidencia.
- Definir tratamiento de diferencia:
  `REENVIO`, `AJUSTE`, `RECLAMACION`.
- Exponer consulta de estado del ciclo de transferencia.

RF cubiertos:

- RF23-RF32
- RF35
- RB04

Estado actual:

- Implementada tabla normalizada `estados_transferencia`, para evitar guardar el
  estado del ciclo como texto suelto en `transferencia`.
- Estados base definidos:
  `SOLICITADA`, `APROBADA`, `ENVIADA`, `RECIBIDA`, `RECIBIDA_PARCIAL`, `RECHAZADA`.
- Implementadas tablas:
  `transferencia`, `detalle_transferencia`, `envio_transferencia`,
  `recepcion_transferencia`, `incidencia_transferencia`.
- Implementados endpoints principales:
  `POST /api/v1/transferencias/crear_transferencia`,
  `POST /api/v1/transferencias/revisar_transferencia/<id_transferencia>`,
  `POST /api/v1/transferencias/registrar_envio_transferencia/<id_transferencia>`,
  `POST /api/v1/transferencias/confirmar_recepcion_transferencia/<id_transferencia>`.
- El despacho descuenta inventario de la sucursal origen y crea movimiento
  `TRANSFERENCIA_SALIDA`.
- La recepcion suma inventario en la sucursal destino y crea movimiento
  `TRANSFERENCIA_ENTRADA`.
- Si la recepcion es parcial, registra faltantes en `incidencia_transferencia`
  con tratamiento `REENVIO`, `AJUSTE` o `RECLAMACION`.

### Fase 4. Completar logistica

Objetivo: que logistica deje de ser solo catalogo.

Tareas:

- Asociar rutas y transportistas a envios de transferencia.
- Registrar fecha estimada y fecha real de llegada.
- Calcular cumplimiento de entrega.
- Consultar transferencias por estado logistico.
- Clasificar rutas por prioridad, costo o tiempo.

RF cubiertos:

- RF33
- RF34
- RF35
- RF36

### Fase 5. Seguridad y actores

Objetivo: alinear backend con los actores documentados.

Tareas:

- Implementar login JWT.
- Proteger endpoints con JWT.
- Crear decorador de roles.
- Aplicar permisos base:
  administrador general, gerente de sucursal y operador de inventario.
- Restringir alcance por sucursal donde aplique.

RNF/RB cubiertos:

- RNF03
- RNF04
- RB01
- RB02
- RB05

### Fase 6. Dashboard y reportes

Objetivo: cubrir analisis, visualizacion y funcionalidad adicional propuesta.

Tareas:

- Endpoint de resumen mensual de ventas.
- Endpoint de rotacion de inventario.
- Productos de alta y baja demanda.
- Productos bajo stock.
- Transferencias activas e impacto en inventario.
- Comparativa entre sucursales para administrador.
- Reportes exportables por rango de fechas y sucursal.

RF cubiertos:

- RF37-RF46

### Fase 7. Calidad para sustentacion

Objetivo: poder defender los flujos sin miedo.

Tareas:

- Agregar tests de recepcion de compra.
- Agregar tests de venta sin stock y venta exitosa.
- Agregar tests de transferencia completa y parcial.
- Documentar endpoints principales en README.
- Documentar uso de IA con ejemplos concretos.
- Revisar Docker Compose de extremo a extremo.

## Orden inmediato recomendado

El siguiente bloque de trabajo deberia ser:

1. Ajustar costo promedio ponderado en recepcion de compras.
2. Implementar venta completa.
3. Implementar transferencia completa.
4. Implementar transferencia parcial con incidencia.
5. Agregar seguridad JWT y roles.
6. Agregar dashboard/reportes.

La razon es simple: compras, ventas y transferencias son los flujos que prueban que el inventario no es solo CRUD, sino un sistema transaccional con trazabilidad.
