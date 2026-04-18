import os
import requests
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from agent import criar_agente
from response import montar_contexto

load_dotenv()

app = Flask(__name__)
agent = criar_agente()

# Ir buscar as variáveis que guardou no ficheiro .env
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")
ACCESS_TOKEN = os.getenv("WHATSAPP_TOKEN")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")

# ---------------------------------------------------------
# ROTA 1 (GET): Serve APENAS para a Meta validar o seu Token
# ---------------------------------------------------------
@app.route("/webhook", methods=["GET"])
def verificar_webhook():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    # Se o token bater certo com o do .env, aceita a verificação
    if mode == "subscribe" and token == VERIFY_TOKEN:
        print("✅ Webhook verificado com sucesso pela Meta!")
        return challenge, 200
    return "Falha na verificação", 403

# ---------------------------------------------------------
# ROTA 2 (POST): Serve para RECEBER as mensagens do cliente
# ---------------------------------------------------------
@app.route("/webhook", methods=["POST"])
def receber_mensagem():
    dados = request.get_json()
    
    try:
        # A Meta envia um JSON muito aninhado. Vamos extrair a mensagem e o número.
        if "entry" in dados and "changes" in dados["entry"][0]:
            valor = dados["entry"][0]["changes"][0]["value"]
            
            if "messages" in valor:
                mensagem_dict = valor["messages"][0]
                telefone_cliente = mensagem_dict["from"]
                texto_usuario = mensagem_dict["text"]["body"]

                print(f"\n📩 Mensagem recebida de {telefone_cliente}: {texto_usuario}")

                # 1. Monta o contexto de produtos
                contexto = montar_contexto(texto_usuario)

                # 2. Prepara o prompt para o Gemini
                prompt = f"""
                INFORMAÇÃO DO SISTEMA: Os produtos disponíveis atualmente na loja para a busca do cliente são:
                {contexto}

                Mensagem do cliente: {texto_usuario}
                """

                # 3. Roda o Agente para obter a resposta
                print("🧠 A pensar na resposta...")
                resposta_ia = agent.run(prompt).content
                print(f"🤖 Resposta gerada: {resposta_ia}")

                # 4. Envia a resposta de volta para o cliente via API da Meta
                enviar_mensagem_meta(telefone_cliente, resposta_ia)

    except Exception as e:
        print("❌ ERRO:", str(e))

    # A Meta exige que o servidor devolva sempre um 200 OK rapidamente
    return jsonify({"status": "ok"}), 200

# ---------------------------------------------------------
# FUNÇÃO DE ENVIO: Comunica com os servidores da Meta
# ---------------------------------------------------------
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
    
    resposta = requests.post(url, json=payload, headers=headers)
    
    if resposta.status_code == 200:
        print("🚀 Resposta enviada com sucesso para o WhatsApp!")
    else:
        print(f"⚠️ Erro ao enviar: {resposta.text}")

if __name__ == "__main__":
    app.run(port=3000, debug=True)