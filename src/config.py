from pathlib import Path

DIR_SRC = Path(__file__).resolve().parent
RUTA_RAIZ = DIR_SRC.parent

R_AGENT = RUTA_RAIZ/"agent"


R_SYSTEM_PROMPT = R_AGENT/"system_prompt.md"