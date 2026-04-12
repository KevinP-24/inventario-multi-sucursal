# Sistema de Inventario Multi-Sucursal

## 1. Descripción del proyecto
Este proyecto corresponde a la prueba técnica para el diseño y desarrollo de un sistema de inventario multi-sucursal. La solución fue planteada para permitir que varias sucursales de una misma organización operen sus transacciones locales de forma independiente, pero compartiendo visibilidad sobre el inventario general de la red.

El sistema contempla procesos de inventario, compras, ventas, transferencias entre sucursales, seguimiento logístico, visualización de indicadores y administración general. Además, incorpora una funcionalidad adicional de reportes exportables en PDF con filtros por rango de fechas y sucursal.

El enfoque del proyecto no se limita a que el sistema funcione, sino a justificar cada decisión de diseño, mantener consistencia entre documentación, arquitectura y modelo de datos, y soportar la operación con trazabilidad.

---

## 2. Objetivo
Diseñar e implementar una solución robusta para la gestión de inventario multi-sucursal, con separación clara entre frontend, backend y base de datos, comunicación por API, ejecución mediante Docker Compose y documentación técnica coherente con la prueba.

---

## 3. Problema que resuelve
En organizaciones con varias sucursales, el control del inventario suele fragmentarse entre sedes. Esto genera problemas de visibilidad, trazabilidad y coordinación operativa, especialmente cuando se requieren transferencias de productos entre sucursales o seguimiento del stock disponible en toda la red.

La solución propuesta busca resolver ese problema mediante:
- autonomía operativa por sucursal,
- visibilidad compartida del inventario general,
- control de ingresos, retiros, compras y ventas,
- gestión de transferencias entre sucursales,
- seguimiento logístico de envíos,
- dashboard con indicadores operativos,
- control administrativo por roles.

---

## 4. Alcance funcional del sistema
El sistema se diseñó para cubrir los siguientes módulos:

### 4.1 Gestión de inventario
- CRUD de productos.
- Consulta de inventario propio y de otras sucursales.
- Registro de ingresos y retiros.
- Control de stock mínimo.
- Alertas de reabastecimiento.
- Manejo de múltiples unidades de medida.
- Historial y trazabilidad de movimientos.

### 4.2 Compras
- Creación y gestión de órdenes de compra.
- Registro de condiciones de compra.
- Confirmación de recepción de mercancía.
- Actualización automática del inventario.
- Histórico por proveedor y por producto.
- Cálculo de costo promedio ponderado.

### 4.3 Ventas
- Registro de ventas por producto, cantidad y precio.
- Asociación de ventas a sucursal, fecha y responsable.
- Validación de stock antes de confirmar la venta.
- Aplicación de descuentos.
- Gestión de listas de precios.
- Generación de comprobantes.

### 4.4 Transferencias entre sucursales
- Solicitud de transferencia.
- Revisión y validación por sucursal origen.
- Aprobación o ajuste de cantidades.
- Registro del envío.
- Confirmación de recepción completa o parcial.
- Registro de faltantes y tratamiento de diferencias.
- Actualización del inventario de las sucursales involucradas.

### 4.5 Logística
- Registro de tiempos estimados y reales de entrega.
- Clasificación de rutas por prioridad, costo o tiempo.
- Seguimiento del estado de transferencias.
- Reportes de cumplimiento logístico por sucursal y por ruta.

### 4.6 Dashboard y análisis
- Volumen de ventas del mes frente a periodos anteriores.
- Rotación de inventario.
- Productos de alta y baja demanda.
- Estado de transferencias activas e impacto en inventario.
- Indicadores de reabastecimiento y productos próximos a agotarse.
- Comparación de rendimiento entre sucursales para perfiles administrativos.

### 4.7 Administración
- Gestión de usuarios.
- Gestión de sucursales.
- Configuración de parámetros generales.
- Consulta de inventario y reportes globales.

### 4.8 Funcionalidad adicional propuesta
**Módulo de reportes exportables**
- Generación de reportes en PDF.
- Filtro por rango de fechas.
- Filtro por sucursal.
- Exportación de reportes de inventario, ventas y transferencias.

---

## 5. Actores del sistema
El sistema contempla tres actores principales:

### 5.1 Administrador general
- Gestiona configuración, usuarios y sucursales.
- Tiene visibilidad global del sistema.
- Supervisa transferencias entre sucursales.
- Consulta reportes globales e indicadores comparativos.

### 5.2 Gerente de sucursal
- Supervisa la operación de una sucursal específica.
- Revisa solicitudes de transferencia.
- Consulta reportes e indicadores operativos.
- Monitorea abastecimiento y productos con bajo stock.

### 5.3 Operador de inventario
- Registra ingresos y retiros de productos.
- Gestiona órdenes de compra y recepción.
- Registra ventas.
- Solicita transferencias.
- Confirma recepciones y registra diferencias.

---

## 6. Arquitectura de la solución
La solución se estructuró con una arquitectura de tres capas:

### 6.1 Frontend
Aplicación web desarrollada con **Angular**, encargada de la interfaz de usuario y de la interacción con la API.

### 6.2 Backend
API REST desarrollada con **Python + Flask**, responsable de:
- validaciones,
- reglas de negocio,
- autenticación,
- autorización,
- sincronización del inventario,
- procesamiento de ventas, compras y transferencias.

### 6.3 Base de datos
Base de datos relacional **PostgreSQL**, utilizada para almacenar la información operativa y mantener integridad, consistencia y trazabilidad.

### 6.4 Infraestructura
La ejecución del sistema se realiza con **Docker Compose**, levantando frontend, backend y base de datos como servicios independientes.

---

## 7. Decisiones técnicas principales
### 7.1 Stack tecnológico seleccionado
- **Frontend:** Angular
- **Backend:** Python con Flask
- **Base de datos:** PostgreSQL
- **Infraestructura:** Docker Compose

### 7.2 Autenticación y autorización
La autenticación se planteó con **JWT**, y la autorización mediante **roles**, de acuerdo con los perfiles del sistema:
- administrador general,
- gerente de sucursal,
- operador de inventario.

### 7.3 Sincronización entre sucursales
La sincronización del inventario se planteó mediante una **base de datos centralizada** y una **única API backend**. Bajo este enfoque, cada ingreso, retiro, compra, venta o transferencia actualiza la información compartida del sistema en tiempo real o near-real-time.

Las validaciones y actualizaciones de existencias se centralizan en el backend, de modo que las operaciones se procesen de forma controlada y consistente, evitando inconsistencias entre sucursales y manteniendo trazabilidad sobre los movimientos registrados.

### 7.4 Patrones de diseño propuestos
- **Service Layer** para centralizar la lógica de negocio.
- **Repository** para desacoplar el acceso a datos de la lógica del sistema.

---

## 8. Modelo de datos
El modelo entidad-relación fue diseñado bajo una estructura relacional centralizada y contempla entidades para:
- administración: rol, usuario, sucursal, parámetros del sistema,
- inventario: producto, unidad de medida, inventario por sucursal, movimientos,
- compras: proveedor, orden de compra, detalle de orden,
- ventas: cliente, lista de precios, venta, detalle de venta,
- transferencias y logística: transferencia, detalle de transferencia, rutas, transportista, envío, recepción e incidencias.

Este diseño permite soportar trazabilidad, operación transaccional y consistencia entre sucursales.

---

## 9. Diagramas y documentación del proyecto
El repositorio incluye la documentación técnica principal del proyecto:

- `Levantamiento de Requerimientos.pdf`
- `Actores del sistema.pdf`
- `Diagrama de actividades.pdf`
- `Diagrama de arquitectura.pdf`
- `Diagrama Entidad relación.pdf`

Diagramas contemplados:
- diagrama de casos de uso,
- diagrama de actividades del flujo de venta,
- diagrama de actividades del flujo de transferencia entre sucursales,
- diagrama de arquitectura,
- diagrama entidad-relación.

Si los archivos se ubican en una carpeta `docs/`, solo ajusta las rutas en el repositorio.

---

## 10. Flujo de ejecución local
### 10.1 Requisitos previos
- Docker
- Docker Compose
- Node.js y npm si se desea usar los scripts de conveniencia del repositorio

### 10.2 Ejecución
```bash
docker compose up --build
```

Para el entorno local de prueba no es necesario crear archivos de entorno manualmente. Las variables requeridas por PostgreSQL y Flask ya están definidas en [docker-compose.yml](/d:/Proyectos/multi-sucursal/docker-compose.yml).

También se puede levantar todo con el script raíz:
```bash
npm run dev
```

Servicios disponibles:
- Frontend Angular: `http://localhost:4200`
- Backend Flask: `http://localhost:5000`
- Health check API: `http://localhost:5000/api/v1/health/`

Para detener los servicios:
```bash
docker compose down
```

O usando el script raíz:
```bash
npm run down
```

### 10.3 Ejecución local del frontend
```bash
cd frontend
npm install
npm start
```

El frontend consume la API desde `http://localhost:5000/api/v1`.

### 10.4 Consideraciones
- La solución está pensada para ejecutarse con un solo comando.
- Frontend, backend y base de datos deben levantarse como servicios independientes.
- La ejecución con Docker Compose no depende de configuración manual del entorno local.

---

## 11. Estructura sugerida del repositorio
```bash
.
├── backend/
├── frontend/
├── docs/
│   ├── Levantamiento de Requerimientos.pdf
│   ├── Actores del sistema.pdf
│   ├── Diagrama de actividades.pdf
│   ├── Diagrama de arquitectura.pdf
│   └── Diagrama Entidad relación.pdf
├── docker-compose.yml
└── README.md
```

Si tu estructura real cambia, ajusta esta sección antes de entregar.

---

## 12. Justificación del diseño
Cada decisión de diseño del proyecto buscó responder tres necesidades del problema:
1. mantener autonomía operativa por sucursal,
2. conservar visibilidad compartida del inventario,
3. asegurar consistencia y trazabilidad sobre las transacciones.

Por eso se adoptó una arquitectura centralizada en backend y base de datos, una separación clara entre capas, un modelo relacional con entidades transaccionales y diagramas orientados a los procesos críticos del sistema.

---

## 13. Uso de Inteligencia Artificial en el Desarrollo
El proyecto utilizó **ChatGPT** como herramienta de apoyo durante el proceso de análisis, estructuración documental, refinamiento de decisiones técnicas y apoyo puntual en la implementación. Su uso no reemplazó la validación manual, sino que sirvió para acelerar la organización del trabajo y mejorar la coherencia entre entregables.

### 13.1 Herramienta de IA utilizada
- **ChatGPT**

### 13.2 Etapas en las que se utilizó
- Definición y refinamiento de requerimientos funcionales y no funcionales.
- Identificación de actores y casos de uso.
- Revisión del flujo de venta y del flujo de transferencia entre sucursales.
- Justificación de arquitectura, autenticación, sincronización y patrones de diseño.
- Apoyo en la redacción del README y de la documentación técnica.
- Revisión de consistencia entre documentos del proyecto.

### 13.3 Ejemplos de prompts utilizados
**Prompt 1**
> Ayúdame a convertir los módulos del sistema en requerimientos funcionales claros, enumerados y alineados con la prueba técnica.

**Resultado obtenido**
Se generó una base inicial de requerimientos funcionales que luego fue revisada y ajustada manualmente para mantener coherencia con el alcance real del proyecto.

**Prompt 2**
> Valida si el diagrama de actividades cumple con el flujo de venta y el flujo de transferencia exigidos en la prueba técnica.

**Resultado obtenido**
Se identificaron vacíos de precisión en el flujo de transferencia, especialmente en la actualización del inventario de sucursal origen y destino, lo que permitió ajustar el texto y el diagrama.

**Prompt 3**
> Contrasta los documentos del proyecto contra la prueba técnica y detecta falencias reales de alineación.

**Resultado obtenido**
Se detectaron ajustes menores en requerimientos, dashboard, logística, sincronización y sección de IA, lo que ayudó a cerrar la coherencia entre los entregables.

### 13.4 Aportes de la IA al proyecto
- Aceleró la estructuración de la documentación.
- Permitió detectar vacíos de trazabilidad entre requerimientos, actores, arquitectura y diagramas.
- Ayudó a refinar la redacción técnica.
- Sirvió como apoyo para revisar consistencia y cerrar detalles de sustentación.

### 13.5 Ajustes manuales realizados
- Revisión completa de los requerimientos para alinearlos con el alcance real de la prueba.
- Corrección manual de numeración, precisión y consistencia entre documentos.
- Ajustes manuales al flujo de transferencia entre sucursales.
- Selección final de decisiones técnicas y redacción adaptada al contexto del proyecto.

### 13.6 Limitaciones encontradas
- Algunas respuestas iniciales resultaron demasiado generales y tuvieron que aterrizarse manualmente.
- Fue necesario validar cada propuesta contra la prueba técnica para evitar agregar funcionalidades no requeridas.
- El resultado generado por IA necesitó revisión para mantener coherencia con la implementación real.

### 13.7 Estimación de uso de IA
Los siguientes porcentajes son **estimados** y deben entenderse como apoyo al proceso, no como reemplazo del criterio técnico:

- **Documentación apoyada por IA:** aproximadamente **65%**.
- **Análisis y estructuración inicial:** aproximadamente **50%**.
- **Código o fragmentos refinados con asistencia de IA:** aproximadamente **25%**.

### 13.8 Evaluación crítica
La IA fue más útil en la organización de la documentación, revisión de consistencia y refinamiento de decisiones técnicas. Su mayor valor estuvo en acelerar tareas repetitivas y servir como apoyo de contraste. Sin embargo, el criterio final de modelado, priorización de cambios y alineación con la prueba tuvo que hacerse manualmente.

---

## 14. Estado del proyecto
Este repositorio reúne la propuesta técnica, el modelado del sistema, la documentación de ingeniería y la base de implementación de la solución. La validez del proyecto se sustenta tanto en el funcionamiento esperado como en la justificación técnica de cada decisión de diseño.

---

## 15. Nota final
La pregunta guía de este proyecto es: **¿por qué se hizo así?**

Por eso, además del código, la solución se apoya en requerimientos claros, actores definidos, diagramas coherentes, arquitectura justificada y documentación alineada con la prueba técnica.
