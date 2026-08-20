from pathlib import Path

DIR_SRC = Path(__file__).resolve().parent
RUTA_RAIZ = DIR_SRC.parent

R_AGENT = RUTA_RAIZ/"agent"
R_MEMORY = RUTA_RAIZ/"memory"
R_MODELS = RUTA_RAIZ/"models"
R_PROTOCOL = RUTA_RAIZ/"protocol"
R_TOOLS = RUTA_RAIZ/"tools"

R_SYSTEM_PROMPT = R_AGENT/"system_prompt.md"