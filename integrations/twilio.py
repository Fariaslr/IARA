from flask import request
from twilio.twiml.messaging_response import MessagingResponse

from services.atendimento import processar_atendimento

def processar_twilio(agent):
    mensagem_usuario = request.form.get("Body")
    telefone =  request.form.get("From")
    
    print(f"📩 Mensagem: {mensagem_usuario}\n📞Número: {telefone}")

    resposta = processar_atendimento(telefone, mensagem_usuario, agent)

    resp = MessagingResponse()
    resp.message(resposta)

    return str(resp)