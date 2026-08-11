from flask import request
from twilio.twiml.messaging_response import MessagingResponse

from service import process_service

def process_twilio(agent):
    """
    Recebe a requisição do Twilio, extrai a mensagem e o número de telefone,
    processa na nossa regra de negócios (IARA) e devolve a resposta formatada.
    """
    user_message = request.form.get("Body")
    phone = request.form.get("From")
    
    print(f"📩 Nova Mensagem: {user_message}\n📞 Número: {phone}")

    ai_response = process_service(phone, user_message, agent)

    twilio_resp = MessagingResponse()
    twilio_resp.message(ai_response)

    return str(twilio_resp)