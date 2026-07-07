# API y Servidor MCP para CENDOJ (Buscador de Jurisprudencia)

Este proyecto proporciona una **API REST (FastAPI)** y un **Servidor MCP (Model Context Protocol)** para buscar y consultar sentencias y resoluciones judiciales del **CENDOJ** (Centro de Documentación Judicial de España).

Dado que el CENDOJ no dispone de una API pública y protege sus búsquedas con Javascript interactivo y validaciones de autocompletado, este servicio utiliza **Playwright** para simular búsquedas reales de forma automatizada y robusta, devolviendo resultados limpios en formato JSON y abstrayendo la descarga y extracción de texto de los PDFs de sentencias.

---

## Características

*   **Buscador Automatizado (Playwright):** Automatiza la navegación, la aceptación del Aviso Legal, la simulación de escritura secuencial para activar el buscador y la selección de la sugerencia del CENDOJ para evitar las limitaciones de búsqueda.
*   **API REST con FastAPI:**
    *   `GET /api/status`: Verifica la salud y configuración del servicio.
    *   `GET /api/search`: Realiza búsquedas avanzadas con parámetros:
        *   `query`: Texto libre opcional.
        *   `fecha_desde` / `fecha_hasta`: Rango de fechas (YYYY-MM-DD o DD/MM/AAAA).
        *   `jurisdiccion`: Civil, Penal, Contencioso-Administrativo, Social, Militar.
        *   `roj`: Identificador ROJ (ej. `STS 2849/2026`).
        *   `ecli`: Código ECLI (ej. `ES:TS:2026:2849`).
        *   `n_resolucion`: Número de resolución.
        *   `n_recurso`: Número de recurso.
        *   `ponente`: Nombre del magistrado ponente.
        *   `norma`: Legislación o norma de interés.
        *   `localizacion`: Lista de localizaciones o Comunidades Autónomas (ej. `Andalucía`, `Cataluña`, `Madrid`).
    *   `GET /api/decision`: Resuelve el contenedor de documentos del CENDOJ, descarga el archivo PDF y extrae su texto plano en español.
*   **Servidor MCP (Model Context Protocol):**
    *   Soporte para modo **Stdio** (para clientes locales de escritorio como Cursor y Claude Desktop).
    *   Soporte para modo **SSE (Server-Sent Events)** montado de forma nativa en FastAPI bajo el prefijo `/mcp` (para clientes remotos o web).
    *   Herramientas expuestas:
        *   `buscar_jurisprudencia`: Realiza búsquedas con todos los filtros detallados (query, roj, ecli, ponente, recurso, resolución, norma, etc.).
        *   `obtener_texto_resolucion`: Descarga un PDF y extrae su texto completo.
*   **Compatibilidad con Windows:** Parcheado para evitar problemas con la política del bucle de eventos (`NotImplementedError` en subprocess) en entornos Windows.

---

## Requisitos Previos

*   Python 3.10 o superior instalado.
*   Navegador Chromium de Playwright instalado en el sistema.

---

## Instalación y Configuración (Rápida)

Para facilitar la configuración en Windows, hemos incluido scripts que automatizan todo el proceso:

1.  **Ejecutar configuración automática:**
    Haz doble clic en el archivo **`setup.bat`** (o ejecútalo desde tu consola). Este script se encargará de:
    *   Crear el entorno virtual `.venv`.
    *   Instalar y actualizar todas las dependencias (`requirements.txt`).
    *   Instalar el navegador Chromium requerido por Playwright.
    *   Crear el archivo de configuración `.env` por defecto.

2.  **Registrar en Clientes MCP (Automático):**
    Una vez finalizado el setup, ejecuta la utilidad de instalación automática para vincular el servidor MCP con tus clientes locales:
    ```powershell
    .venv\Scripts\python.exe install_mcp.py
    ```
    Este comando detectará la ruta absoluta de tu repositorio y **registrará automáticamente** el servidor CENDOJ en las configuraciones globales de:
    *   **Claude Desktop** (`claude_desktop_config.json`)
    *   **Antigravity IDE** (`mcp_config.json`)

---

## Instalación y Configuración Manual (Alternativa)

Si no deseas utilizar los scripts de automatización, puedes inicializar el proyecto manualmente siguiendo estos pasos:

1.  **Crear el entorno virtual de Python:**
    ```powershell
    python -m venv .venv
    ```

2.  **Activar el entorno virtual:**
    *   **En Windows (PowerShell):**
        ```powershell
        .venv\Scripts\Activate.ps1
        ```
    *   **En macOS/Linux o Git Bash:**
        ```bash
        source .venv/bin/activate
        ```

3.  **Instalar dependencias:**
    ```powershell
    pip install --upgrade pip
    pip install -r requirements.txt
    ```

4.  **Instalar el navegador Chromium para Playwright:**
    ```powershell
    playwright install chromium
    ```

5.  **Crear el archivo de configuración `.env`:**
    Crea un archivo llamado `.env` en la raíz del proyecto y escribe la siguiente línea:
    ```env
    CENDOJ_HEADLESS=true
    ```

---

## Guía de Ejecución

El script `run.py` es el punto de entrada unificado:

### 1. Ejecutar como API REST y Servidor SSE (FastAPI)
Para levantar el servidor web:
```powershell
.venv\Scripts\python.exe run.py api
```
El servidor se iniciará en **http://localhost:8000**.
*   **Documentación Interactiva (Swagger/OpenAPI):** Visita [http://localhost:8000/docs](http://localhost:8000/docs) para interactuar directamente con la API REST.
*   **Endpoint de MCP SSE:** Accesible en [http://localhost:8000/mcp/sse](http://localhost:8000/mcp/sse).

### 2. Ejecutar como Servidor MCP Stdio (Consola/Entrada Estándar)
Para iniciar el servidor MCP utilizando la entrada y salida estándar (ideal para integrar en herramientas de escritorio locales):
```powershell
.venv\Scripts\python.exe run.py mcp
```

---

## Integración Manual con Clientes MCP (Opcional)

Si prefieres realizar el registro de manera manual en lugar de usar `install_mcp.py`:

### Claude Desktop
Para conectar este servidor MCP con Claude Desktop, edita tu archivo de configuración `claude_desktop_config.json` (usualmente en `%APPDATA%\Claude\claude_desktop_config.json` en Windows) y añade la configuración del servidor:

```json
{
  "mcpServers": {
    "cendoj-jurisprudencia": {
      "command": "c:/workspace-github/CENDOJ-BOE/.venv/Scripts/python.exe",
      "args": ["c:/workspace-github/CENDOJ-BOE/run.py", "mcp"],
      "env": {
        "CENDOJ_HEADLESS": "true"
      }
    }
  }
}
```

### Cursor
Para utilizar el servidor en Cursor:
1.  Ve a **Settings > Features > MCP**.
2.  Haz clic en **+ Add New MCP Server**.
3.  Configura los siguientes valores:
    *   **Name:** `CENDOJ`
    *   **Type:** `command`
    *   **Command:** `c:/workspace-github/CENDOJ-BOE/.venv/Scripts/python.exe c:/workspace-github/CENDOJ-BOE/run.py mcp`

---

## Pruebas y Verificación

El proyecto incluye scripts en el directorio temporal o de scratchpad para pruebas de desarrollo rápidas:
*   **Prueba de Scraper Directo:** `test_scraper.py` busca un término e intenta descargar el primer PDF.
*   **Prueba de API REST e Integración SSE:** `test_api.py` verifica el estado, realiza una consulta y ejecuta la descarga del PDF a través del servidor FastAPI en ejecución.
*   **Prueba de Cliente MCP Stdio:** `test_mcp_stdio_client.py` inicia el servidor MCP en un subproceso y realiza las llamadas JSON-RPC oficiales simulando un cliente real.
