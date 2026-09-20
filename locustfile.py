from locust import HttpUser, task, between

class IaraLoadTest(HttpUser):
    # Simula o tempo que um utilizador demora a digitar entre mensagens
    wait_time = between(1, 3)

    @task
    def testar_webhook(self):
        # Simula a estrutura do payload que o Twilio envia para o teu Flask
        payload = {
            "From": "whatsapp:+5511999999999",
            "Body": "Olá, quero comprar um amigurumi polvo"
        }
        # Dispara a requisição POST para a rota que criaste no main.py
        self.client.post("/whatsapp", data=payload)