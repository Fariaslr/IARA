from flask import Flask
from dotenv import load_dotenv

from agent import criar_agente
from integrations.twilio import processar_twilio

load_dotenv()

app = Flask(__name__)
agent = criar_agente()


@app.route("/whatsapp", methods=["POST"])
def whatsapp():
    return processar_twilio(agent)


if __name__ == "__main__":
    app.run(port=3000, debug=True)