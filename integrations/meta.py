import os
import requests

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")
ACCESS_TOKEN = os.getenv("WHATSAPP_TOKEN")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")


def verificar_token_meta(request):
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        print("✅ Webhook verificado!")
        return challenge, 200

    return "Erro na verificação", 403


def tratar_status_meta(valor):
    if "statuses" in valor:
        status = valor["statuses"][0]
        print(f"📡 Status: {status.get('status')}")

        if "errors" in status:
            erro = status["errors"][0]
            print(f"❌ Meta erro: {erro.get('title')}")


def enviar_mensagem_meta(para, texto):
    url = f"https://graph.facebook.com/v19.0/{PHONE_NUMBER_ID}/messages"

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "messaging_product": "whatsapp",
        "to": para,
        "type": "text",
        "text": {"body": texto}
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        print("🚀 Enviado!")
    else:
        print(f"⚠️ Erro: {response.text}")