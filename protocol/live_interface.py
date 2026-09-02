import asyncio
import pyaudio
from google.genai import types
from .base_interface import BaseInterface

AUDIO_FORMAT = pyaudio.paInt16
CHANNELS = 1
INPUT_SAMPLE_RATE = 16000
OUTPUT_SAMPLE_RATE = 24000
CHUNK_SIZE = 1024


class LiveInterface(BaseInterface):
    def __init__(self, client):
        self.client = client
        self.model = "gemini-3.1-flash-tts-preview"

    def start(self, chat=None):
        asyncio.run(self._run_live_session())

    async def _run_live_session(self):
        p = pyaudio.PyAudio()

        # Configuración corregida usando strings directos
        live_config = types.LiveConnectConfig(
            response_modalities=["AUDIO"],
            speech_config=types.SpeechConfig(
                voice_config=types.VoiceConfig(
                    prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name="Kore")
                )
            ),
        )

        print("\n--- Modo Live Iniciado: Habla por el micrófono (Ctrl+C para salir) ---")

        async with self.client.aio.live.connect(model=self.model, config=live_config) as session:
            async def send_mic_audio():
                input_stream = p.open(
                    format=AUDIO_FORMAT,
                    channels=CHANNELS,
                    rate=INPUT_SAMPLE_RATE,
                    input=True,
                    frames_per_buffer=CHUNK_SIZE,
                )
                try:
                    while True:
                        data = input_stream.read(CHUNK_SIZE, exception_on_overflow=False)
                        await session.send(
                            input={"data": data, "mime_type": "audio/pcm"},
                            end_of_turn=False,
                        )
                        await asyncio.sleep(0.001)
                except asyncio.CancelledError:
                    pass
                finally:
                    input_stream.stop_stream()
                    input_stream.close()

            async def play_gemini_audio():
                output_stream = p.open(
                    format=AUDIO_FORMAT,
                    channels=CHANNELS,
                    rate=OUTPUT_SAMPLE_RATE,
                    output=True,
                    frames_per_buffer=CHUNK_SIZE,
                )
                try:
                    async for response in session.receive():
                        server_content = response.server_content
                        if server_content and server_content.model_turn:
                            for part in server_content.model_turn.parts:
                                if part.inline_data:
                                    output_stream.write(part.inline_data.data)
                except asyncio.CancelledError:
                    pass
                finally:
                    output_stream.stop_stream()
                    output_stream.close()

            try:
                await asyncio.gather(send_mic_audio(), play_gemini_audio())
            except KeyboardInterrupt:
                print("\nFinalizando Modo Live...")
            finally:
                p.terminate()