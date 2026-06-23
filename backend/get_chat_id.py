from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from telegram_bot import TelegramBot


def main() -> None:
    print("Obteniendo chat_id de usuarios que escribieron al bot...\n")

    bot = TelegramBot()

    print(f"  Bot: @{bot.get_me()['result']['username']}")
    print(f"  Token configurado: {bot.token[:8]}...{bot.token[-4:]}\n")

    print("  Pidiendo a cada medico que envie /start al bot en Telegram.")
    print("  Luego ejecuta este script para ver su chat_id.\n")

    try:
        updates = bot.get_updates()
    except Exception as e:
        print(f"  Error al obtener updates: {e}")
        print("  Si nadie le ha escrito al bot, getUpdates puede retornar vacio.")
        return

    if not updates:
        print("  No hay mensajes recientes. Pide a cada medico que:")
        print("    1. Busque el bot en Telegram")
        print("    2. Envie /start (o cualquier mensaje)")
        print("    3. Vuelva a ejecutar este script")
        return

    seen: set[str] = set()
    print(f"  {'Chat ID':<18} {'Nombre':<25} {'Usuario'}")
    print(f"  {'-'*18} {'-'*25} {'-'*20}")

    for u in updates:
        msg = u.get("message") or u.get("channel_post")
        if not msg:
            continue
        chat = msg.get("chat", {})
        chat_id = str(chat.get("id", ""))
        if not chat_id or chat_id in seen:
            continue
        seen.add(chat_id)

        first_name = chat.get("first_name", "")
        last_name = chat.get("last_name", "")
        full_name = f"{first_name} {last_name}".strip()
        username = chat.get("username", "")

        print(f"  {chat_id:<18} {full_name:<25} @{username}")

    if not seen:
        print("  (sin chats con mensajes)")
    else:
        print(f"\n  {len(seen)} chat(s) encontrado(s).")
        print("  Copia el chat_id correspondiente a la columna 'telegram_chat_id'")
        print("  del Google Sheet para cada medico.")


if __name__ == "__main__":
    main()
