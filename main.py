import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

from src.config import R_SYSTEM_PROMPT

from tools.weather_tool import get_current_weather
from tools.datetime_tool import get_current_time

from agent.dataConfig import cargar_system_prompt
from protocol.console_interface import ConsoleInterface
from protocol.tts_interface import TTSInterface
from protocol.live_interface import LiveInterface


load_dotenv()
client = genai.Client()


def main():
    print("Agente listo. Escribe tu consulta (o 'salir' para finalizar):")
    system_instruction_text = cargar_system_prompt()

    chat = client.chats.create( #Se puede cambiar con client.models.generatecontent pero en ese caso no se puede llamar a funciones
        model="gemini-3.6-flash", #Escoges el modelo según lo que te convenga
        #contents=input(), #El texto que se le envía al modelo (disponible solo para client.models.gen)
        config=types.GenerateContentConfig(
            system_instruction=system_instruction_text, #las instrucciones que el modelo tiene en cuenta para su funcionamiento(system_prompt)
            tools=[get_current_time, get_current_weather],
            temperature=0.7 #Esto mientras mas bajo hace al modelo más determinista, enfocado y predecible(0-0.3). Mientras más alto es más creativo, diverso y abierto el modelo (0.7-1). En algunos modelos se puede llegar a 2, revisar si lo permite el modelo y si es conveniente
        )
    )

    #interfaz = ConsoleInterface() #Cambio de Interfaz según se necesite
    #interfaz = TTSInterface(client)
    interfaz = LiveInterface(client)
    interfaz.start(chat)

if __name__ == "__main__":
    main()