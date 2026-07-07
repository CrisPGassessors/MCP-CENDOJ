@echo off
echo ==============================================
echo  Configuracion Inicial - CENDOJ API & MCP
echo ==============================================
echo.

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python no esta instalado o no se encuentra en el PATH.
    echo Por favor, instala Python 3.10+ y vuelve a intentarlo.
    pause
    exit /b 1
)

:: Create virtual environment if it doesn't exist
if not exist .venv (
    echo [INFO] Creando entorno virtual .venv...
    python -m venv .venv
) else (
    echo [INFO] El entorno virtual .venv ya existe.
)

:: Install dependencies
echo [INFO] Instalando dependencias de requirements.txt...
.venv\Scripts\python.exe -m pip install --upgrade pip
.venv\Scripts\pip.exe install -r requirements.txt

:: Install Playwright Chromium
echo [INFO] Instalando navegador Chromium de Playwright...
.venv\Scripts\playwright.exe install chromium

:: Create default .env if missing
if not exist .env (
    echo [INFO] Creando archivo de configuracion .env por defecto...
    echo # Configuración de CENDOJ Scraper> .env
    echo CENDOJ_HEADLESS=true>> .env
)

echo.
echo ==============================================
echo  Instalacion Completada con Exito!
echo ==============================================
echo.
echo Para registrar el servidor MCP en Claude Desktop y Antigravity, ejecuta:
echo   .venv\Scripts\python.exe install_mcp.py
echo.
pause
