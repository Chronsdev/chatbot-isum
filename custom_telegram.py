# custom_telegram.py
import logging
import os
import asyncio
from rasa.core.channels.channel import InputChannel
from sanic import Blueprint, response
from sanic.request import Request
from typing import Text, Dict, Any, Optional, Awaitable

logger = logging.getLogger(__name__)

class RailwayTelegramInput(InputChannel):
    """Canal de Telegram optimizado para Railway que evita el error del event loop"""
    
    @classmethod
    def name(cls) -> Text:
        return "telegram"

    def __init__(
        self,
        access_token: Text,
        verify: Text,
        webhook_url: Text,
    ) -> None:
        self.access_token = access_token
        self.verify = verify
        self.webhook_url = webhook_url

    def blueprint(self, on_new_message: callable) -> Blueprint:
        telegram_webhook = Blueprint("telegram_webhook")
        
        @telegram_webhook.route("/", methods=["GET"])
        async def health(_: Request) -> Any:
            return response.json({"status": "telegram_webhook_ready"})

        @telegram_webhook.route("/webhook", methods=["GET", "POST"])
        async def message(request: Request) -> Any:
            if request.method == "GET":
                return response.text("Telegram webhook operational")
            
            try:
                # Procesar el mensaje sin verificación de credenciales
                request_data = request.json
                if not request_data:
                    return response.text("No data", status=400)
                
                # Extraer información del mensaje
                sender_id = self._extract_sender_id(request_data)
                text_content = self._extract_text(request_data)
                
                if sender_id and text_content:
                    # Crear el mensaje para Rasa
                    await on_new_message({
                        "sender_id": sender_id,
                        "text": text_content,
                        "metadata": self._get_metadata(request),
                    })
                
                return response.text("success")
                
            except Exception as e:
                logger.error(f"Error procesando mensaje de Telegram: {e}")
                return response.text("error", status=500)

        return telegram_webhook

    def _extract_sender_id(self, request_data: Dict) -> Optional[Text]:
        """Extraer sender_id del mensaje de Telegram"""
        try:
            if "message" in request_data:
                return str(request_data["message"]["from"]["id"])
            elif "callback_query" in request_data:
                return str(request_data["callback_query"]["from"]["id"])
        except (KeyError, TypeError) as e:
            logger.warning(f"Error extrayendo sender_id: {e}")
        return None

    def _extract_text(self, request_data: Dict) -> Optional[Text]:
        """Extraer texto del mensaje de Telegram"""
        try:
            if "message" in request_data:
                return request_data["message"].get("text", "")
            elif "callback_query" in request_data:
                return request_data["callback_query"].get("data", "")
        except (KeyError, TypeError) as e:
            logger.warning(f"Error extrayendo texto: {e}")
        return None

    def _get_metadata(self, request: Request) -> Dict[Text, Any]:
        """Obtener metadata del request"""
        return {
            "out_channel": self.name(),
            "webhook_url": self.webhook_url
        }