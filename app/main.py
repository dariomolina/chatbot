import os

from dotenv import load_dotenv
from fastapi import (
    FastAPI,
    HTTPException,
    Depends,
    Request
)

from chat import ChatManager, ChatAPI
from validations import validate_token

load_dotenv()
app = FastAPI()

chat_manager = ChatManager()
chat_api = ChatAPI(chat_manager)


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
    try:
        message_data = data.get("entry", [])[0].get("changes", [])[0].get("value", {}).get("messages", [])[0]
        phone_number_id = message_data.get("from", "")
        message_text = message_data.get("text", "").get("body")
        response_message = chat_api.process_message(phone_number_id, message_text)
        chat_api.send_response(to=phone_number_id, message_text=response_message)
    except Exception:
        raise HTTPException(status_code=403, detail="Error")


@app.get("/webhooks")
async def get_webhook(request: Request):
    query_params = dict(request.query_params.items())
    hub_challenge = query_params.get("hub.challenge")
    hub_verify_token = query_params.get("hub.verify_token")
    Depends(validate_token)
    try:
        if hub_verify_token == os.getenv("TOKEN"):
            return int(hub_challenge)
        else:
            raise HTTPException(status_code=403, detail="Token de verificación incorrecto")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error en el servidor")


@app.post("/v1/media")
async def post_media(request: Request):
    return {"status": "ok"}
