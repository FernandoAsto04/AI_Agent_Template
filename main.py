import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client()

def main():
    print("Inicializando Agente de IA...")

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents="Esta es una prueba de la API de gemini, di algo corto"
    )
    
    print("\nRespuesta del modelo:")
    print(response.text)

if __name__ == "__main__":
    main()