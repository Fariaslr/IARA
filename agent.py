from agno.agent import Agent
from agno.models.google import Gemini


def criar_agente():
    return Agent(
        id="atendente-humanizado",
        name="Atendente WhatsApp",
        role="Atender clientes de forma humanizada",
        instructions="""
        Você é atendente de uma bomboniere.

        - Seja simpático
        - Respostas curtas
        - Faça perguntas
        - Nunca invente produtos
        - Não exagere em emojis
        """,
        model=Gemini(id="gemini-2.5-flash"),
    )