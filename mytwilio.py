import os
from twilio.rest import Client
import json

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_NUMBER = os.getenv("TWILIO_WHATSAPP_NUMBER")
TWILIO_MESSAGE_SERVICE_SID = os.getenv("TWILIO_MESSAGE_SERVICE_SID")
TWILIO_PEDIDO_CRIADO_TEMPLATE = os.getenv("TWILIO_PEDIDO_CRIADO_TEMPLATE")

# Cria o cliente Twilio
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)


# Envia uma mensagem via WhatsApp usando a API Twilio.
def send_message(to: str, body: str):
    message = client.messages.create(
        body=body, from_=TWILIO_WHATSAPP_NUMBER, to=f"whatsapp:+55{to}"
    )

    print(f"mensagem de whats enviada!")
    print(message)

    return message.sid


# Envia uma mensagem via WhatsApp usando a API Twilio com template
def whats_pedido_criado(to: str, codigo_pedido: str):
    message = client.messages.create(
        content_sid=TWILIO_PEDIDO_CRIADO_TEMPLATE,
        to=f"whatsapp:+55{to}",
        from_=TWILIO_WHATSAPP_NUMBER,
        content_variables=json.dumps({"1": codigo_pedido}),
        messaging_service_sid=TWILIO_MESSAGE_SERVICE_SID,
    )
    return message.sid


# Envia um SMS usando a API Twilio
def envia_sms(to: str, mensagem: str):
    from twilio.rest import Client

    account_sid = TWILIO_ACCOUNT_SID
    auth_token = TWILIO_AUTH_TOKEN

    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        body=mensagem, to=f"+55{to}", messaging_service_sid=TWILIO_MESSAGE_SERVICE_SID
    )
    return message.sid
