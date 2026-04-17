from agno.agent import Agent
from agno.models.google import Gemini
from dotenv import load_dotenv
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

load_dotenv()

app = Flask(__name__)

agent = Agent(
    id="atendente-humanizado",
    name="Atendente de mensagem no WhatsApp",
    role="Você tem a responsabilidade de atender os clientes de maneira humanizada e simples",
    instructions="""
    Você é um atendente de uma bomboniere.

    Contexto:
    - A loja vende doces, chocolates, balas e guloseimas
    - O atendimento é feito via WhatsApp
    - Os clientes querem saber preços, produtos e fazer pedidos

    Comportamento:
    - Seja simpático e próximo
    - Use linguagem simples e natural
    - Evite respostas robóticas
    - Use emojis moderados 😊

    Objetivo:
    - Ajudar o cliente
    - Sugerir produtos
    - Conduzir para uma compra
    """,
    model=Gemini(id="gemini-2.5-flash-lite"),
)

@app.route("/whatsapp", methods=["POST"])
def whatsapp():
    mensagem_usuario = request.form.get("Body")
    resposta_ia = agent.run(mensagem_usuario).content

    resp = MessagingResponse()
    resp.message(resposta_ia)

    return str(resp)

if __name__ == "__main__":
    app.run(port=3000)