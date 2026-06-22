import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from telegram_bot import TelegramBot


def main() -> None:
    print("Probando conexión con Telegram Bot API...\n")

    try:
        bot = TelegramBot()
        print(f"  Token configurado: {bot.token[:8]}...{bot.token[-4:]}")
        print(f"  Chat ID por defecto: {bot.default_chat_id}")

        print("\n  Verificando token con getMe...")
        me = bot.get_me()
        bot_info = me["result"]
        print(f"    Bot username: @{bot_info['username']}")
        print(f"    Bot name: {bot_info['first_name']}")
        print(f"    Bot ID: {bot_info['id']}")

        print("\n  Enviando mensaje de prueba...")
        response = bot.send_test_message()
        if response["ok"]:
            print("    Mensaje enviado correctamente.")
            print(
                f"    Entregado a chat_id: {response['result']['chat']['id']}"
            )
        else:
            print(f"    Error en el envío: {response}")

        print("\n  Conexión exitosa con Telegram Bot API.")

    except Exception as e:
        print(f"\n  Error: {e}")
        print("\n  Revisa docs/telegram_bot_setup.md para la configuración.")
        raise


if __name__ == "__main__":
    main()
