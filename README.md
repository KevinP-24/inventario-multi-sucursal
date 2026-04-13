````md
# Multi-sucursal

Sistema de inventario multi-sucursal desarrollado como solución para la prueba técnica de OptiPlant Consultores. La aplicación permite gestionar inventario, compras, ventas, transferencias entre sucursales, logística y visualización de indicadores, manteniendo autonomía operativa por sede y visibilidad compartida sobre el inventario general de la red.

## Objetivo del proyecto

Diseñar e implementar una solución robusta para la gestión de inventario de múltiples sucursales, cumpliendo con separación de capas entre frontend, backend y base de datos, comunicación mediante API REST y despliegue completo con Docker Compose.

## Alcance funcional

La solución cubre los módulos principales solicitados para la prueba técnica:

### Gestión de inventario
- gestión de productos
- consulta de inventario por sucursal
- consulta de inventario de otras sucursales
- ingresos y retiros de inventario
- control de stock mínimo
- trazabilidad de movimientos
- manejo de múltiples unidades de medida

### Compras
- creación y gestión de órdenes de compra
- registro de condiciones de compra
- recepción de mercancía
- actualización automática del inventario
- histórico de compras
- cálculo de costo promedio ponderado

### Ventas
- registro de ventas
- validación de disponibilidad de stock
- aplicación de descuentos
- manejo de listas de precios
- generación de comprobantes

### Transferencias entre sucursales
- solicitud de transferencias
- validación de disponibilidad en sucursal origen
- aprobación o ajuste de cantidades
- registro de envío
- confirmación de recepción completa o parcial
- registro de faltantes y diferencias

### Logística
- tiempos estimados y reales de entrega
- clasificación de rutas
- seguimiento del estado de transferencias
- reportes de cumplimiento logístico

### Dashboard
- comparativa de ventas
- indicadores de inventario
- productos de alta y baja demanda
- estado de transferencias activas
- indicadores de reabastecimiento
- comparativa entre sucursales para perfiles administrativos

## Arquitectura de la solución

La solución fue construida bajo una arquitectura de tres capas:

- **Frontend:** Angular
- **Backend:** Python + Flask
- **Base de datos:** PostgreSQL
- **Infraestructura:** Docker Compose

### Separación de responsabilidades

- El frontend se encarga exclusivamente de la capa de presentación.
- El backend centraliza la lógica del negocio, validaciones, reglas de inventario, compras, ventas y transferencias.
- PostgreSQL gestiona la persistencia, consistencia y trazabilidad de la información.
- Docker Compose orquesta todos los servicios del sistema con un solo comando.

## Decisiones técnicas principales

### Frontend: Angular
Se eligió Angular por su estructura modular, su organización para aplicaciones administrativas y su facilidad para separar la capa de presentación de la lógica del negocio.

### Backend: Python con Flask
Se eligió Flask por su ligereza y claridad para construir una API REST capaz de centralizar validaciones, reglas operativas y procesamiento transaccional sin agregar complejidad innecesaria.

### Base de datos: PostgreSQL
Se eligió PostgreSQL porque el sistema maneja información relacional y transaccional, con necesidad de mantener consistencia, integridad y trazabilidad en operaciones de inventario, compras, ventas y transferencias.

### Infraestructura: Docker Compose
Se adoptó Docker Compose para permitir la ejecución integral del sistema con un solo comando, dejando frontend, backend y base de datos como servicios independientes y aislados.

### Autenticación y autorización
La autenticación se implementó mediante JWT. La autorización se gestiona por roles, restringiendo el acceso a funciones según el nivel de responsabilidad de cada usuario.

### Sincronización entre sucursales
La sincronización del inventario entre sucursales se resuelve mediante una base de datos centralizada y una única API de backend. Bajo este enfoque, cada ingreso, retiro, compra, venta o transferencia actualiza la información compartida del sistema en tiempo real o near-real-time.

### Patrones de diseño
En el backend se aplicó una organización orientada a separación de responsabilidades, apoyándose en una capa de servicios para la lógica de negocio y una capa de acceso a datos para mantener el código más claro, desacoplado y mantenible.

## Modelo base del sistema

A nivel administrativo, el sistema se apoya principalmente en tres entidades base:

- **Rol**
- **Sucursal**
- **Usuario**

Estas entidades permiten controlar permisos, trazabilidad y alcance operativo dentro de la plataforma.

## Roles base de acceso

El sistema incluye tres perfiles principales de prueba:

### Administrador general
- **Correo:** `admin.general@multisucursal.local`
- **Contraseña:** `Admin123*`

### Admin sucursal
- **Correo:** `admin.sucursal@multisucursal.local`
- **Contraseña:** `Sucursal123*`

### Operario de inventario
- **Correo:** `operario.inventario@multisucursal.local`
- **Contraseña:** `Inventario123*`

## Puesta en marcha

Para crear todo desde cero y levantar el entorno completo en una máquina virgen, ejecuta desde la raíz del proyecto:

```powershell
docker compose up --build -d
````

También puedes usar el lanzador incluido:

```powershell
.\start.ps1
```

Alternativa en `cmd`:

```bat
start.cmd
```

## ¿Qué hace el arranque?

Este proceso:

* construye las imágenes
* crea la base de datos
* aplica migraciones
* carga datos iniciales
* levanta backend y frontend

## Requisitos

* Docker Desktop instalado y encendido

## Estructura general del proyecto

```text
/
├── backend/
├── frontend/
├── database/
├── docker-compose.yml
├── start.ps1
├── start.cmd
└── README.md
```

## Diagramas de ingeniería

El repositorio incluye los diagramas requeridos por la prueba técnica:

* diagrama de casos de uso
* diagrama de actividades
* diagrama de arquitectura
* diagrama entidad-relación

## Reglas de negocio relevantes

* una venta no debe confirmarse si no existe stock disponible
* toda transferencia entre sucursales debe quedar registrada y trazable
* las sucursales operan de forma independiente en sus transacciones locales
* el inventario se gestiona de forma centralizada para mantener consistencia entre sucursales
* el acceso a las funciones del sistema depende del rol del usuario

## Uso de inteligencia artificial en el desarrollo

Durante el desarrollo del proyecto se utilizaron herramientas de inteligencia artificial como un apoyo importante para avanzar con mayor velocidad, validar coherencia entre entregables y acelerar tareas repetitivas de implementación.

### Herramientas utilizadas

* **ChatGPT (OpenAI):** se utilizó para validar coherencia entre documentos, revisar consistencia entre requerimientos, actores, módulos, flujos y modelo de datos, y apoyar la redacción y organización de la documentación técnica.
* **Codex (OpenAI):** se utilizó para construir estructuras repetitivas de código, apoyar la definición de esqueletos base del proyecto, montar la estructura inicial del modelo de base de datos propuesto y apoyar la configuración inicial de la infraestructura Docker para levantar toda la solución con un solo comando.
* **Claude (Anthropic):** se utilizó para validaciones rápidas de estilos CSS, contraste visual de componentes y revisión ágil de consistencia en secciones frontend.

### Etapas en las que se aplicó IA

Las herramientas de IA se utilizaron principalmente en:

* validación de coherencia entre documentación técnica y módulos del sistema
* organización de la estructura del README y de los documentos de soporte
* construcción de estructuras repetitivas de implementación
* apoyo en la definición inicial del modelo de datos
* apoyo en la estructura inicial de Docker e integración del arranque del entorno
* revisión rápida de estilos y consistencia visual en frontend

### Ejemplos concretos de uso

#### Ejemplo 1: coherencia documental

**Objetivo:** contrastar requerimientos, actores, casos de uso y entidades para verificar que el sistema estuviera alineado con la prueba técnica.

**Resultado:** permitió detectar vacíos, ajustar relaciones entre módulos y mejorar la consistencia entre documentos antes de cerrar la entrega.

#### Ejemplo 2: estructura base de backend y base de datos

**Objetivo:** acelerar la construcción de estructuras repetitivas y partir de una base ordenada para módulos, entidades y relaciones iniciales.

**Resultado:** se obtuvo una base inicial útil para el proyecto, que posteriormente fue ajustada manualmente para reflejar las reglas reales del sistema.

#### Ejemplo 3: infraestructura Docker

**Objetivo:** estructurar la base de la infraestructura para levantar frontend, backend y base de datos con un solo comando.

**Resultado:** sirvió como punto de partida para organizar la configuración inicial del entorno y acelerar la puesta en marcha del proyecto.

#### Ejemplo 4: revisión visual rápida

**Objetivo:** validar estilos CSS y coherencia visual de componentes frontend.

**Resultado:** permitió detectar ajustes rápidos de presentación y mantener una interfaz más consistente.

### Evaluación crítica del uso de IA

La IA fue útil para acelerar la documentación, contrastar consistencia entre entregables, construir bases iniciales de implementación y reducir tiempo en tareas repetitivas. También aportó velocidad en la definición inicial del modelo de datos, la estructura del proyecto y la infraestructura Docker.

Sin embargo, fue necesario ajustar manualmente aspectos clave como:

* reglas de negocio finales
* permisos por rol
* relaciones definitivas del modelo de datos
* validaciones operativas de compras, ventas y transferencias
* decisiones finales de diseño y comportamiento real del sistema

La IA aportó velocidad y apoyo estructural, pero la validación final y los ajustes críticos del proyecto se realizaron manualmente.

### Estimación de asistencia de IA

Estimación aproximada del apoyo de IA en el proyecto:

* **coherencia documental y organización técnica:** 30%
* **estructuras repetitivas de código y soporte de implementación:** 50%
* **estructura inicial del modelo de base de datos e infraestructura Docker:** 30%
* **validación visual rápida y estilos CSS:** 10%

## Historias de usuario representativas

* Como operador de inventario, quiero registrar ingresos de productos con su precio de compra para mantener actualizado el costo promedio del inventario.
* Como administrador de sucursal, quiero consultar indicadores de ventas e inventario para tomar decisiones de abastecimiento.
* Como operario de inventario, quiero solicitar transferencias entre sucursales para cubrir faltantes de producto en mi sede.

## Estado del proyecto

Proyecto estructurado para ejecutarse con Docker Compose, con separación de capas, autenticación por roles, módulos principales del dominio y documentación alineada con los entregables solicitados en la prueba técnica.

```
```
