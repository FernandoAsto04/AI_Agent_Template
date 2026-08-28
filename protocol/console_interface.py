from .base_interface import BaseInterface

class ConsoleInterface(BaseInterface):
    def start(self, chat):
        print("\n--- Modo Consola Iniciado ---")
        while True:
            user_input = input("\nTú: ").strip()
            if user_input.lower() in ["salir", "exit", "quit"]:
                print("Cerrando sesión...")
                break
            if not user_input:
                continue

            try:
                response = chat.send_message(user_input)
                print(f"\nAgente: {response.text}")
            except Exception as e:
                print(f"\n[Error]: {e}")