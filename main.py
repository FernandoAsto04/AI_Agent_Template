import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

from src.config import R_SYSTEM_PROMPT

load_dotenv()

client = genai.Client()

def cargar_system_prompt() -> str:
    with open(R_SYSTEM_PROMPT, "r", encoding="UTF-8") as f:
        template = f.read()

    
    config_datos = {
        "agent_name": "DevAssistant",
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

def main():
    print("Inicializando Agente de IA...")
    system_instruction_text = cargar_system_prompt()

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=input(),
        config=types.GenerateContentConfig(
            system_instruction=system_instruction_text,  # <- Aquí inyectas tu prompt agnóstico
            temperature=0.3
        )
    )
    
    print("\nRespuesta del modelo:")
    print(response.text)

if __name__ == "__main__":
    main()