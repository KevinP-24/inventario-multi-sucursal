# Multi-sucursal

Para crear todo desde cero y levantar todo el entorno en una maquina virgen, ejecuta un solo comando desde la raiz del proyecto:

```powershell
docker compose up --build -d
```

Si prefieres usar el lanzador incluido:

```powershell
.\start.ps1
```

Alternativa en `cmd`:

```bat
start.cmd
```

Ese comando:

- construye las imagenes
- crea la base de datos
- aplica migraciones
- carga datos iniciales
- levanta backend y frontend

Requisitos:

- Docker Desktop instalado y encendido
