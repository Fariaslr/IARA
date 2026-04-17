# 🤖 Bot de Atendimento WhatsApp com Agno + Gemini

Bot de atendimento automatizado para WhatsApp usando o framework Agno, modelo Gemini e Twilio como intermediário.

---

## 📋 Pré-requisitos

- Python 3.10+
- Conta no [Twilio](https://twilio.com) (gratuita)
- Chave de API do [Google AI Studio](https://aistudio.google.com) (Gemini)
- [Cloudflare Tunnel](https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/) ou ngrok

---

## 📁 Estrutura do Projeto

```
customer-support-ai/
├── main.py        # Código principal do bot
├── .env           # Variáveis de ambiente (não commitar!)
├── .env.example   # Exemplo de variáveis
└── requirements.txt
```

---

## ⚙️ Instalação

**1. Clone o repositório e entre na pasta:**
```bash
git clone <url-do-repositorio>
cd customer-support-ai
```

**2. Crie e ative o ambiente virtual:**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

**3. Instale as dependências:**
```bash
pip install agno flask twilio google-generativeai python-dotenv
```

---

## 🔑 Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
GOOGLE_API_KEY=sua_chave_do_gemini_aqui
```

> Para obter a chave do Gemini, acesse [aistudio.google.com](https://aistudio.google.com) → Get API Key.

---

## 🚀 Como Rodar

### Passo 1 — Suba o servidor Flask

Abra um terminal e rode:
```bash
python main.py
```

Você verá:
```
* Running on http://127.0.0.1:3000
```

---

### Passo 2 — Exponha o servidor com Cloudflare Tunnel

Abra **outro terminal** e rode:
```bash
cloudflared tunnel --url http://localhost:3000
```

Copie a URL gerada, parecida com:
```
https://xyz.trycloudflare.com
```

> ⚠️ Essa URL muda toda vez que você reiniciar o Cloudflare. Atualize no Twilio sempre que isso acontecer.

---

### Passo 3 — Configure o Webhook no Twilio

1. Acesse [console.twilio.com](https://console.twilio.com)
2. Vá em **Messaging → Try it out → Send a WhatsApp message**
3. Role até **Sandbox Configuration**
4. No campo **"When a message comes in"**, cole:
```
https://xyz.trycloudflare.com/whatsapp
```
5. Certifique que o método está como **POST**
6. Clique em **Save**

---

### Passo 4 — Ative o Sandbox no seu WhatsApp

Na mesma tela do Twilio, você verá um número e uma mensagem para enviar, tipo:
```
join <palavra-chave>
```

Abra o WhatsApp no celular, mande essa mensagem para o número indicado e aguarde a confirmação.

---

### Passo 5 — Teste!

Mande qualquer mensagem para o número do Twilio Sandbox pelo WhatsApp.

Se aparecer no terminal do Flask:
```
"POST /whatsapp HTTP/1.1" 200 -
```
Está funcionando! ✅

---

## 🧠 Código Principal (`main.py`)

```python
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
```

---

## 🔄 Fluxo de Funcionamento

```
Seu celular (WhatsApp)
        ↓
  Número do Twilio Sandbox
        ↓
  Cloudflare Tunnel (URL pública)
        ↓
  Flask rodando na porta 3000
        ↓
  Agente Agno + Gemini
        ↓
  Resposta volta para o WhatsApp
```

---

## ❗ Problemas Comuns

| Problema | Causa | Solução |
|----------|-------|---------|
| `405 Method Not Allowed` | Acessou a URL pelo navegador | Normal — a rota só aceita POST |
| `500 Internal Server Error` | Erro no código Python | Veja os logs do terminal Flask |
| Bot não responde | Webhook não configurado | Verifique a URL no Twilio |
| URL do Cloudflare mudou | Reiniciou o tunnel | Atualize a URL no Twilio |
| `MessagingResponse` não encontrado | Twilio não instalado | `pip install twilio` |

---

## 🌐 Indo para Produção

Quando o bot estiver pronto e você quiser usar um número real:

1. Acesse [developers.facebook.com/apps](https://developers.facebook.com/apps)
2. Crie um App → **Other** → **Business** → adicione o produto **WhatsApp**
3. Registre o número desejado (ele sairá do WhatsApp pessoal)
4. Substitua o Twilio pela Meta API direta
5. Use um servidor real (Railway, Render, VPS) no lugar do Cloudflare Tunnel

> ⚠️ Ao registrar um número na Meta API, ele deixa de funcionar no WhatsApp pessoal. Use um número exclusivo para o bot.

---

## 📦 `requirements.txt`

```
agno
flask
twilio
google-generativeai
python-dotenv
```

Gerar automaticamente:
```bash
pip freeze > requirements.txt
```