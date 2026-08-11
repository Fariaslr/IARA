from flask import Flask
from dotenv import load_dotenv

from agent import create_agent
from database import create_table
from integrations.twilio import process_twilio

load_dotenv()

app = Flask(__name__)
agent = create_agent()

@app.route("/whatsapp", methods=["POST"])
def whatsapp():
    return process_twilio(agent)

if __name__ == "__main__":
    create_table()
    
    app.run(port=3000, debug=True)