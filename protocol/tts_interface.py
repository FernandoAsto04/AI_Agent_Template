from .base_interface import BaseInterface
from google import genai
import wave
import base64
import winsound
import os

class TTSInterface(BaseInterface):
    def __init__(self, client):
        self.client = client

    def _save_wave_file(self, filename: str, pcm: bytes, channels: int = 1, rate: int = 24000, sample_width: int = 2):
        #Guarda los bytes PCM en un archivo .wav reproducible.
        with wave.open(filename, "wb") as wf:
            wf.setnchannels(channels)
            wf.setsampwidth(sample_width)
            wf.setframerate(rate)
            wf.writeframes(pcm)

    def _speak_gemini(self, text: str):
        #Envía el texto al modelo de TTS de Gemini y reproduce el audio resultante.
        try:
            interaction = self.client.interactions.create(
                model="gemini-3.1-flash-tts-preview",
                input=text,
                response_format={"type": "audio"},
                generation_config={
                    "speech_config": [
                        {"voice": "Kore"}  # Opciones comunes: Kore, Puck, Fenrir, Aoede
                    ]
                }
            )

            # Decodificar el audio y guardarlo
            audio_bytes = base64.b64decode(interaction.output_audio.data)
            output_file = "response_temp.wav"
            self._save_wave_file(output_file, audio_bytes)

            # Reproducir el audio en Windows de forma síncrona
            winsound.PlaySound(output_file, winsound.SND_FILENAME)

        except Exception as e:
            print(f"\n[Error en TTS]: {e}")

    def start(self, chat):
        print("---Modo consolo + Gemini TTS activado---")
        while True:
            user_input = input("\nTú: ")
            if user_input in ["salir", "exit", "quit"]:
                print("Cerrando sesión...")
                break
            if not user_input:
                continue
        
            try:
                response = chat.send_message(user_input)
                print(f"\nAgente: {response.text}")
                self._speak_gemini(response.text)
            except Exception as e:
                print("f\n[Error temporal]: {e}")