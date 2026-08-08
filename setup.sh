#!/bin/bash
echo "=============================================="
echo " Configuracion Inicial - CENDOJ API & MCP (Unix)"
echo "=============================================="
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python 3 no está instalado o no se encuentra en el PATH."
    echo "Por favor, instala Python 3.10+ y vuelve a intentarlo."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "[INFO] Creando entorno virtual .venv..."
    python3 -m venv .venv
else
    echo "[INFO] El entorno virtual .venv ya existe."
fi

# Install dependencies
echo "[INFO] Instalando dependencias de requirements.txt..."
.venv/bin/python -m pip install --upgrade pip
.venv/bin/pip install -r requirements.txt

# Install Playwright Chromium
echo "[INFO] Instalando navegador Chromium de Playwright..."
.venv/bin/playwright install chromium

# Create default .env if missing
if [ ! -f ".env" ]; then
    echo "[INFO] Creando archivo de configuración .env por defecto..."
    echo "# Configuración de CENDOJ Scraper" > .env
    echo "CENDOJ_HEADLESS=true" >> .env
fi

echo ""
echo "=============================================="
echo " ¡Instalación Completada con Éxito!"
echo "=============================================="
echo ""
echo "Para registrar el servidor MCP en Claude Desktop y Antigravity, ejecuta:"
echo "  .venv/bin/python install_mcp.py"
echo ""
