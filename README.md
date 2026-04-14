# Multi-sucursal

Sistema de inventario multi-sucursal desarrollado como solucion para la prueba tecnica de OptiPlant Consultores. La aplicacion permite gestionar inventario, compras, ventas, transferencias entre sucursales, logistica y visualizacion de indicadores, manteniendo autonomia operativa por sede y visibilidad compartida sobre el inventario general de la red.

## Objetivo del proyecto

Disenar e implementar una solucion robusta para la gestion de inventario de multiples sucursales, cumpliendo con separacion de capas entre frontend, backend y base de datos, comunicacion mediante API REST y despliegue completo con Docker Compose.

## Alcance funcional

La solucion cubre los modulos principales solicitados para la prueba tecnica:

### Gestion de inventario

* gestion de productos
* consulta de inventario por sucursal
* consulta de inventario de otras sucursales
* ingresos y retiros de inventario
* control de stock minimo
* trazabilidad de movimientos
* manejo de multiples unidades de medida

### Compras

* creacion y gestion de ordenes de compra
* registro de condiciones de compra
* recepcion de mercancia
* actualizacion automatica del inventario
* historico de compras
* calculo de costo promedio ponderado

### Ventas

* registro de ventas
* validacion de disponibilidad de stock
* aplicacion de descuentos
* manejo de listas de precios
* generacion de comprobantes

### Transferencias entre sucursales

* solicitud de transferencias
* validacion de disponibilidad en sucursal origen
* aprobacion o ajuste de cantidades
* registro de envio
* confirmacion de recepcion completa o parcial
* registro de faltantes y diferencias

### Logistica

* tiempos estimados y reales de entrega
* clasificacion de rutas
* seguimiento del estado de transferencias
* reportes de cumplimiento logistico

### Dashboard

* comparativa de ventas
* indicadores de inventario
* productos de alta y baja demanda
* estado de transferencias activas
* indicadores de reabastecimiento
* comparativa entre sucursales para perfiles administrativos

## Arquitectura de la solucion

La solucion fue construida bajo una arquitectura de tres capas:

* Frontend: Angular
* Backend: Python con Flask
* Base de datos: PostgreSQL
* Infraestructura: Docker Compose

### Separacion de responsabilidades

* El frontend se encarga exclusivamente de la capa de presentacion.
* El backend centraliza la logica del negocio, validaciones, reglas de inventario, compras, ventas y transferencias.
* PostgreSQL gestiona la persistencia, consistencia y trazabilidad de la informacion.
* Docker Compose orquesta todos los servicios del sistema con un solo comando.

## Decisiones tecnicas principales

### Frontend: Angular

Se eligio Angular por su estructura modular, su organizacion para aplicaciones administrativas y su facilidad para separar la capa de presentacion de la logica del negocio.

### Backend: Python con Flask

Se eligio Flask por su ligereza y claridad para construir una API REST capaz de centralizar validaciones, reglas operativas y procesamiento transaccional sin agregar complejidad innecesaria.

### Base de datos: PostgreSQL

Se eligio PostgreSQL porque el sistema maneja informacion relacional y transaccional, con necesidad de mantener consistencia, integridad y trazabilidad en operaciones de inventario, compras, ventas y transferencias.

### Infraestructura: Docker Compose

Se adopto Docker Compose para permitir la ejecucion integral del sistema con un solo comando, dejando frontend, backend y base de datos como servicios independientes y aislados.

### Autenticacion y autorizacion

La autenticacion se implemento mediante JWT. La autorizacion se gestiona por roles, restringiendo el acceso a funciones segun el nivel de responsabilidad de cada usuario.

### Sincronizacion entre sucursales

La sincronizacion del inventario entre sucursales se resuelve mediante una base de datos centralizada y una unica API de backend. Bajo este enfoque, cada ingreso, retiro, compra, venta o transferencia actualiza la informacion compartida del sistema en tiempo real o near real time.

### Patrones de diseno

En el backend se aplico una organizacion orientada a separacion de responsabilidades, apoyandose en una capa de servicios para la logica de negocio y una capa de acceso a datos para mantener el codigo mas claro, desacoplado y mantenible.

## Modelo base del sistema

A nivel administrativo, el sistema se apoya principalmente en tres entidades base:

* Rol
* Sucursal
* Usuario

Estas entidades permiten controlar permisos, trazabilidad y alcance operativo dentro de la plataforma.

## Roles base de acceso

El sistema incluye tres perfiles principales de prueba:

### Administrador general

Correo: [admin.general@multisucursal.local](mailto:admin.general@multisucursal.local)
Contrasena: Admin123*

### Admin sucursal

Correo: [admin.sucursal@multisucursal.local](mailto:admin.sucursal@multisucursal.local)
Contrasena: Sucursal123*

### Operario de inventario

Correo: [operario.inventario@multisucursal.local](mailto:operario.inventario@multisucursal.local)
Contrasena: Inventario123*

## Puesta en marcha

Para crear todo desde cero y levantar el entorno completo en una maquina virgen, ejecuta desde la raiz del proyecto:

docker compose up --build -d

Tambien puedes usar el lanzador incluido:

start.ps1

Alternativa en cmd:

start.cmd

## Que hace el arranque

Este proceso:

* construye las imagenes
* crea la base de datos
* aplica migraciones
* carga datos iniciales
* levanta backend y frontend

## Requisitos

* Docker Desktop instalado y encendido

## Estructura general del proyecto

/
backend/
frontend/
database/
docker-compose.yml
start.ps1
start.cmd
README.md

## Diagramas de ingenieria

El repositorio incluye los diagramas requeridos por la prueba tecnica como archivos separados dentro de la carpeta de documentacion:

* Actores del sistema y diagrama de casos de uso
* Diagrama de actividades
* Diagrama de arquitectura
* Diagrama Entidad relacion final

Adicionalmente, se incluye el documento de Levantamiento de Requerimientos y el documento de Historias de Usuario como soporte complementario del modelado y la trazabilidad funcional del sistema.

## Reglas de negocio relevantes

* una venta no debe confirmarse si no existe stock disponible
* toda transferencia entre sucursales debe quedar registrada y trazable
* las sucursales operan de forma independiente en sus transacciones locales
* el inventario se gestiona de forma centralizada para mantener consistencia entre sucursales
* el acceso a las funciones del sistema depende del rol del usuario

## Uso de inteligencia artificial en el desarrollo

Durante el desarrollo del proyecto se utilizaron herramientas de inteligencia artificial como un apoyo importante para avanzar con mayor velocidad, validar coherencia entre entregables y acelerar tareas repetitivas de implementacion.

### Herramientas utilizadas

* ChatGPT de OpenAI: se utilizo para validar coherencia entre documentos, revisar consistencia entre requerimientos, actores, modulos, flujos y modelo de datos, y apoyar la redaccion y organizacion de la documentacion tecnica.
* Codex de OpenAI: se utilizo para construir estructuras repetitivas de codigo, apoyar la definicion de esqueletos base del proyecto, montar la estructura inicial del modelo de base de datos propuesto y apoyar la configuracion inicial de la infraestructura Docker para levantar toda la solucion con un solo comando.
* Claude de Anthropic: se utilizo para validaciones rapidas de estilos CSS, contraste visual de componentes y revision agil de consistencia en secciones frontend.

### Etapas en las que se aplico IA

Las herramientas de IA se utilizaron principalmente en:

* validacion de coherencia entre documentacion tecnica y modulos del sistema
* organizacion de la estructura del README y de los documentos de soporte
* construccion de estructuras repetitivas de implementacion
* apoyo en la definicion inicial del modelo de datos
* apoyo en la estructura inicial de Docker e integracion del arranque del entorno
* revision rapida de estilos y consistencia visual en frontend

### Evidencia de uso de IA: prompts y resultados obtenidos

A continuacion se documentan algunos prompts representativos utilizados durante el desarrollo del proyecto, junto con el resultado obtenido y el ajuste manual realizado posteriormente.

#### Ejemplo 1: coherencia entre documentos del proyecto

Herramienta utilizada: ChatGPT
Objetivo: validar coherencia entre requerimientos, actores, casos de uso, historias de usuario y modelo de datos.

Prompt representativo:
Contrasta estos entregables de la prueba tecnica: levantamiento de requerimientos, actores del sistema, diagrama entidad relacion y flujos. Dime que modulos, actores, tablas o relaciones faltan, cuales sobran y que cambios exactos debo hacer para que todo quede alineado con la prueba.

Resultado obtenido:
La IA ayudo a detectar inconsistencias entre actores, modulos y entidades, ademas de senalar vacios entre el documento de requerimientos y el modelo de datos.

Ajuste manual realizado:
Se corrigieron manualmente relaciones del modelo E R, responsabilidades de actores, flujos de transferencia y alcance real de algunos modulos para mantener coherencia con la implementacion final.

#### Ejemplo 2: estructura base de backend y modelo inicial de datos

Herramienta utilizada: Codex
Objetivo: acelerar la construccion de estructuras repetitivas de codigo y partir de una base organizada para modulos, entidades y relaciones iniciales.

Prompt representativo:
Genera una estructura base para un sistema de inventario multi sucursal con backend Flask y PostgreSQL. Incluye organizacion por modulos, entidades principales, relaciones iniciales, separacion entre rutas, servicios y acceso a datos.

Resultado obtenido:
Se obtuvo una base inicial util para estructurar el proyecto, acelerar la creacion de archivos repetitivos y organizar la primera version del modelo de datos.

Ajuste manual realizado:
Fue necesario modificar manualmente entidades, relaciones, nombres de tablas, reglas operativas y permisos para reflejar el comportamiento real del sistema y los requerimientos de la prueba.

#### Ejemplo 3: infraestructura Docker y levantamiento con un solo comando

Herramienta utilizada: Codex
Objetivo: estructurar una base de infraestructura para levantar frontend, backend y base de datos con Docker Compose.

Prompt representativo:
Genera un docker compose para un proyecto con frontend Angular, backend Flask y PostgreSQL. El entorno debe levantar todos los servicios con un solo comando, esperar disponibilidad de la base de datos, ejecutar migraciones y cargar datos semilla.

Resultado obtenido:
La IA sirvio como punto de partida para definir la estructura inicial del archivo docker-compose.yml y organizar el flujo de arranque del entorno.

Ajuste manual realizado:
Se adaptaron manualmente variables de entorno, comandos de migracion, seed de datos, puertos, nombres de contenedores y dependencias entre servicios hasta obtener una configuracion funcional para el proyecto.

#### Ejemplo 4: revision visual rapida de frontend

Herramienta utilizada: Claude
Objetivo: revisar estilos CSS, contraste visual y consistencia de componentes frontend.

Prompt representativo:
Analiza este HTML y CSS de un modulo administrativo. Indica problemas de espaciado, jerarquia visual, consistencia de botones, tablas y formularios. Propon cambios puntuales sin alterar la estructura general del componente.

Resultado obtenido:
La IA permitio identificar ajustes rapidos de presentacion, mejorar consistencia visual y detectar detalles de estilo que afectaban la claridad de algunos modulos.

Ajuste manual realizado:
La aplicacion final de estilos, validacion visual real y decisiones de UI se hicieron manualmente sobre los componentes implementados.

### Evaluacion critica del uso de IA

La IA fue util como apoyo para acelerar documentacion, detectar inconsistencias entre entregables, proponer estructuras iniciales de codigo, sugerir una base para el modelo de datos y servir como punto de partida para la infraestructura Docker y ajustes visuales del frontend.

Su mayor aporte estuvo en la velocidad de analisis, organizacion tecnica y construccion inicial de artefactos repetitivos. Tambien ayudo a reducir tiempo en tareas de contraste documental y en la preparacion de estructuras base sobre las cuales se trabajo posteriormente de forma manual.

Sin embargo, la IA no reemplazo la validacion tecnica del proyecto. Fue necesario ajustar manualmente aspectos criticos como:

* reglas de negocio finales
* permisos por rol
* relaciones definitivas del modelo de datos
* validaciones operativas de compras, ventas y transferencias
* comportamiento real de inventario por sucursal
* decisiones finales de diseno, arquitectura y experiencia de usuario

La IA fue un acelerador del proceso, pero las decisiones finales del proyecto, la correccion del comportamiento funcional y la consistencia entre implementacion y documentacion se resolvieron manualmente.

### Limitaciones observadas en el uso de IA

Durante el desarrollo se identificaron algunos limites claros en el apoyo de IA:

* en varios casos propuso estructuras correctas a nivel general, pero no completamente alineadas con las reglas especificas de la prueba
* algunas relaciones o permisos sugeridos debieron corregirse para ajustarse al flujo real del sistema
* las respuestas utiles requerian validacion constante para evitar inconsistencias entre documentacion, backend y modelo de datos
* en frontend, varias sugerencias servian como guia, pero necesitaban revision visual real antes de aplicarse

### Estimacion de asistencia de IA

Estimacion aproximada del apoyo de IA en el proyecto:

* coherencia documental y organizacion tecnica: 30 %
* estructuras repetitivas de codigo y soporte de implementacion: 60 %
* estructura inicial del modelo de base de datos e infraestructura Docker: 30 %
* validacion visual rapida y estilos CSS: 10 %

En terminos globales, la asistencia de IA se utilizo principalmente como apoyo de aceleracion y validacion, pero no sustituyo la toma de decisiones ni el ajuste manual de la solucion final.
