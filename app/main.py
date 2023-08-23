from fastapi import FastAPI, HTTPException, Depends, Header, Query, Request
from pydantic import BaseModel
from typing import List
import requests

from chat import ChatManager, EmailService, ChatAPI



app = FastAPI()

expected_token = "pinchilita-458"  # Cambia esto por tu token secreto

@app.get("/")
async def initial():
    return {"message": "lalala"}

# Clase de modelo para el mensaje
class Message(BaseModel):
    from_: str
    id: str
    timestamp: str
    type: str
    text: dict

# Clase de modelo para los cambios en el webhook
class WebhookChange(BaseModel):
    field: str
    value: dict

# Clase de modelo para la entrada del webhook
class WebhookEntry(BaseModel):
    id: str
    changes: List[WebhookChange]

# Clase de modelo para los datos del webhook
class WebhookData(BaseModel):
    object: str
    entry: List[WebhookEntry]

# Función para validar el token en la cabecera
def validate_token(authorization: str = Header(...)):
    if authorization != f"Bearer {expected_token}":
        raise HTTPException(status_code=401, detail="Token no válido")
    return True



chat_manager = ChatManager()
email_service = EmailService()
chat_api = ChatAPI(chat_manager, email_service)


@app.post("/webhooks")
async def post_webhook(request: Request):
    """
    https://developers.facebook.com/docs/whatsapp/cloud-api/webhooks/components
    {
        "object": "whatsapp_business_account",
        "entry": [{
            "id": "WHATSAPP-BUSINESS-ACCOUNT-ID",
            "changes": [{
                "value": {
                    "messaging_product": "whatsapp",
                    "metadata": {
                        "display_phone_number": "PHONE-NUMBER",
                        "phone_number_id": "PHONE-NUMBER-ID"
                    },
                    # Additional arrays and objects
                    "contacts": [{...}]
                    "errors": [{...}]
                    "messages": [{...}]
                    "statuses": [{...}]},
               "field": "messages"
            }]
        }]
    }
    """
    data = await request.json()
    from pprint import pprint
    pprint(data)
    try:
        message_data = data.get("entry", [])[0].get("changes", [])[0].get("value", {}).get("messages", [])[0]
        phone_number_id = message_data.get("from", "")
        message_text = message_data.get("text", "").get("body")
        response_message = chat_api.process_message(phone_number_id, message_text)
        chat_api.send_response(to=phone_number_id, message_text=response_message)
    except:
        raise HTTPException(status_code=403, detail="Error")


@app.get("/webhooks")
async def get_webhook(request: Request):
    query_params = dict(request.query_params.items())
    hub_mode = query_params.get("hub.mode")
    hub_challenge = query_params.get("hub.challenge")
    hub_verify_token = query_params.get("hub.verify_token")

    print(hub_mode, hub_challenge, hub_verify_token)
    Depends(validate_token)

    try:
        if hub_verify_token == "pinchilita-458":
            return int(hub_challenge)
        else:
            raise HTTPException(status_code=403, detail="Token de verificación incorrecto")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error en el servidor")


@app.post("/v1/media")
async def post_media(request: Request):
    return {"status": "ok"}
