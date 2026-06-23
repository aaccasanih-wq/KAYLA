from __future__ import annotations

import os
from typing import Any

import requests
from dotenv import load_dotenv

load_dotenv()


class TelegramBot:
    """Cliente para enviar mensajes por Telegram usando la Bot API."""

    def __init__(
        self,
        token: str | None = None,
        default_chat_id: str | None = None,
    ) -> None:
        self.token = token or os.getenv("TELEGRAM_BOT_TOKEN")
        self.default_chat_id = default_chat_id or os.getenv(
            "TELEGRAM_CHAT_ID_MEDICO"
        )

        if not self.token:
            raise ValueError(
                "TELEGRAM_BOT_TOKEN no está configurado. "
                "Agrega el token del bot en .env"
            )

        self.api_base = f"https://api.telegram.org/bot{self.token}"

    def send_message(
        self,
        text: str,
        chat_id: str | None = None,
        parse_mode: str | None = None,
        disable_notification: bool = False,
    ) -> dict[str, Any]:
        """Envía un mensaje de texto a un chat de Telegram.

        Returns:
            Respuesta de la API de Telegram como dict.
        """
        target_chat = chat_id or self.default_chat_id
        if not target_chat:
            raise ValueError(
                "No se especificó chat_id y TELEGRAM_CHAT_ID_MEDICO no está configurado."
            )

        payload: dict[str, Any] = {
            "chat_id": target_chat,
            "text": text,
            "disable_notification": disable_notification,
        }
        if parse_mode:
            payload["parse_mode"] = parse_mode

        response = requests.post(
            f"{self.api_base}/sendMessage", data=payload, timeout=30
        )
        response.raise_for_status()
        return response.json()

    def send_reminder(
        self,
        reminder_text: str,
        chat_id: str | None = None,
    ) -> dict[str, Any]:
        """Envía un mensaje de recordatorio con formato Markdown."""
        return self.send_message(
            text=reminder_text,
            chat_id=chat_id,
            parse_mode="Markdown",
        )

    def get_me(self) -> dict[str, Any]:
        """Verifica que el token sea válido. Retorna info del bot."""
        response = requests.get(f"{self.api_base}/getMe", timeout=30)
        response.raise_for_status()
        return response.json()

    def get_updates(self, timeout: int = 0) -> list[dict[str, Any]]:
        """Obtiene los updates (mensajes) recientes recibidos por el bot.

        Útil para descubrir el chat_id de usuarios que le escribieron al bot.
        """
        response = requests.get(
            f"{self.api_base}/getUpdates",
            params={"timeout": timeout},
            timeout=timeout + 5,
        )
        response.raise_for_status()
        return response.json().get("result", [])

    def get_chat_info(self, chat_id: str | None = None) -> dict[str, Any]:
        """Obtiene información sobre un chat."""
        target_chat = chat_id or self.default_chat_id
        if not target_chat:
            raise ValueError("chat_id es requerido para get_chat_info")

        response = requests.get(
            f"{self.api_base}/getChat",
            params={"chat_id": target_chat},
            timeout=30,
        )
        response.raise_for_status()
        return response.json()

    def send_test_message(
        self, chat_id: str | None = None
    ) -> dict[str, Any]:
        """Envía un mensaje de prueba simple."""
        text = (
            "*KAYLA - Mensaje de prueba*\n"
            "Si recibes este mensaje, la configuración del bot es correcta."
        )
        return self.send_message(
            text=text, chat_id=chat_id, parse_mode="Markdown"
        )
