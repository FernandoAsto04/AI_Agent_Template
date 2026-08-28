from src.config import R_SYSTEM_PROMPT

def cargar_system_prompt() -> str:
    with open(R_SYSTEM_PROMPT, "r", encoding="UTF-8") as f:
        template = f.read()

    
    config_datos = {
        "agent_name": "DevAssist",
        "domain": "desarrollo de software y APIs",
        "primary_objective": "ayudar a estructurar código de forma limpia",
        "target_audience": "desarrolladores",
        "user_expertise": "intermedio",
        "allowed_behaviors": "dar ejemplos claros y precisos, mantener una estructura lógica, priorizar buenas prácticas",
        "forbidden_behaviors": "inventar información técnica, asumir conocimientos no declarados, proporcionar respuestas vagas",
        "tone": "técnico y directo",
        "language": "Español"
    }

    return template.format(**config_datos)