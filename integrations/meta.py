import os
import requests

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")
ACCESS_TOKEN = os.getenv("WHATSAPP_TOKEN")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")

def verify_meta_token(request):
    """
    Valida o webhook junto ao painel de desenvolvedores da Meta.
    Garante que apenas o Facebook/Meta consiga se conectar à nossa API.
    """
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        print("✅ Webhook verificado com sucesso!")
        return challenge, 200

    return "Erro na verificação do token", 403

def handle_meta_status(value):
    """
    Processa recibos de leitura e status de entrega das mensagens.
    Monitora silenciosamente se a mensagem chegou ou deu erro.
    """
    if "statuses" in value:
        status = value["statuses"][0]
        print(f"📡 Status da mensagem: {status.get('status')}")

        if "errors" in status:
            error = status["errors"][0]
            print(f"❌ Erro reportado pela Meta: {error.get('title')}")

def send_meta_message(to, text):
    """
    Envia a resposta da IARA de volta para o cliente da Maresia Crochê via WhatsApp.
    """
    url = f"https://graph.facebook.com/v19.0/{PHONE_NUMBER_ID}/messages"

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": text}
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        print("🚀 Mensagem enviada com sucesso!")
    else:
        print(f"⚠️ Falha ao enviar mensagem: {response.text}")