import os
import json
import sys

def get_config_paths():
    appdata = os.environ.get("APPDATA", "")
    userprofile = os.environ.get("USERPROFILE", "")
    
    claude_path = os.path.join(appdata, "Claude", "claude_desktop_config.json")
    antigravity_path = os.path.join(userprofile, ".gemini", "antigravity-ide", "mcp_config.json")
    
    return claude_path, antigravity_path

def register_in_config(config_path, server_name, python_exe, run_py):
    if not config_path:
        return False
        
    print(f"Buscando archivo de configuración: {config_path}")
    
    # Read existing config
    config_dir = os.path.dirname(config_path)
    if not os.path.exists(config_dir):
        try:
            os.makedirs(config_dir, exist_ok=True)
        except Exception as e:
            print(f"No se pudo crear el directorio {config_dir}: {e}")
            return False
            
    config_data = {}
    if os.path.exists(config_path):
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                config_data = json.load(f)
        except Exception as e:
            print(f"Error al leer {config_path} (se creará uno nuevo): {e}")
            
    # Ensure mcpServers dictionary exists
    if "mcpServers" not in config_data:
        config_data["mcpServers"] = {}
        
    # Configure the CENDOJ server
    config_data["mcpServers"][server_name] = {
        "command": python_exe.replace("\\", "/"),
        "args": [run_py.replace("\\", "/"), "mcp"],
        "env": {
            "CENDOJ_HEADLESS": "true"
        }
    }
    
    # Write back config
    try:
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(config_data, f, indent=2, ensure_ascii=False)
        print(f"[OK] Servidor MCP registrado en: {config_path}")
        return True
    except Exception as e:
        print(f"[ERROR] No se pudo escribir en {config_path}: {e}")
        return False

def main():
    # Detect current repository paths
    project_dir = os.path.abspath(os.path.dirname(__file__))
    python_exe = os.path.join(project_dir, ".venv", "Scripts", "python.exe")
    run_py = os.path.join(project_dir, "run.py")
    
    print("==============================================")
    
    if not os.path.exists(python_exe):
        print(f"[ERROR] No se encontró el entorno virtual en: {python_exe}")
        print("Por favor, ejecuta primero 'setup.bat' para configurar el entorno.")
        sys.exit(1)
        
    print(f"Ruta del proyecto detectada: {project_dir}")
    print(f"Ejecutable Python detectado: {python_exe}")
    
    claude_path, antigravity_path = get_config_paths()
    
    # Register in Claude Desktop
    register_in_config(claude_path, "cendoj-jurisprudencia", python_exe, run_py)
    
    # Register in Antigravity IDE
    register_in_config(antigravity_path, "cendoj-jurisprudencia", python_exe, run_py)
    
    print("==============================================")
    print("¡Registro completado!")
    print("Si tienes Claude Desktop o el IDE abierto, por favor reinícialos para aplicar los cambios.")

if __name__ == "__main__":
    main()
