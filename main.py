import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

from src.config import R_SYSTEM_PROMPT

from tools.weather_tool import get_current_weather
from tools.datetime_tool import get_current_time

load_dotenv()

client = genai.Client()

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

def main():
    print("Agente listo. Escribe tu consulta (o 'salir' para finalizar):")
    system_instruction_text = cargar_system_prompt()

    chat = client.chats.create( #Se puede cambiar con client.models.generatecontent pero en ese caso no se puede llamar a funciones
        model="gemini-3.6-flash", #Escoges el modelo según lo que te convenga
        #contents=input(), #El texto que se le envía al modelo xd (disponible solo para client.models.gen)
        config=types.GenerateContentConfig(
            system_instruction=system_instruction_text, #las instrucciones que el modelo tiene en cuenta para su funcionamiento(system_prompt)
            tools=[get_current_time, get_current_weather],
            temperature=0.7 #Esta vaina mientras mas baja hace al modelo más determinista, enfocado y predecible(0-0.3). Mientras más alto es más creativo, diverso y abierto el modelo (0.7-1). En algunos modelos se puede llegar a 2, revisar si lo permite el modelo y si es conveniente
        )
    )

    while True:
        user_input = input("\nTú: ").strip()
        
        if user_input.lower() in ["salir", "exit", "quit"]:
            print("Cerrando sesión del agente...")
            break
            
        if not user_input:
            continue

        
        try:
            response = chat.send_message(user_input)
            print("\nRespuesta del modelo:")
            print(response.text)
        except Exception as e:
            print(f"\n[Error temporal del servidor]: {e}\nIntenta enviar el mensaje nuevamente.")

if __name__ == "__main__":
    main()