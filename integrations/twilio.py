from flask import request
from twilio.twiml.messaging_response import MessagingResponse

from response import montar_contexto


def processar_twilio(agent):
    mensagem_usuario = request.form.get("Body")

    print(f"📩 Mensagem: {mensagem_usuario}")

    contexto = montar_contexto(mensagem_usuario)

    prompt = f"""
    Produtos disponíveis:
    {contexto}

    Mensagem do cliente: {mensagem_usuario}
    """

    resposta_ia = agent.run(prompt).content

    resp = MessagingResponse()
    resp.message(resposta_ia)

    return str(resp)