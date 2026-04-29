from state import obter_estado, atualizar_etapa
from response import montar_contexto

def processar_atendimento(telefone, mensagem, agent):
    estado = obter_estado(telefone)
    etapa_atual = estado["etapa"]

    # 1. A Persona Base (Isso nunca muda)
    instrucoes_base = """Você é um atendente de uma bomboniere, focado em um atendimento humano, empático e amigável.
    Regras gerais de comportamento:
    - Seja natural e não pareça um robô.
    - Use no máximo 1 emoji por mensagem.
    - Nunca invente produtos que não estão listados no catálogo.
    - Seja conciso e direto ao ponto.
    """

    # 2. Definir o Objetivo do Agente baseado na etapa
    objetivo_etapa = ""
    contexto_produtos = ""

    if etapa_atual == "inicio":
        objetivo_etapa = "O cliente iniciou a conversa agora. Cumprimente-o calorosamente e apresente as categorias principais da loja (chocolates, balas e sem açúcar). Termine perguntando o que ele deseja hoje."
        atualizar_etapa(telefone, "categoria")

    elif etapa_atual == "categoria":
        contexto_produtos = montar_contexto(mensagem)
        
        objetivo_etapa = """O cliente está procurando doces específicos.
        Siga estas regras rigorosamente:
        1. Verifique se o doce que o cliente pediu está no [CATÁLOGO DISPONÍVEL].
        2. Se o produto NÃO ESTIVER no catálogo (ex: ele pediu jujuba e só temos bala Fini), seja honesto. Peça desculpas gentilmente, informe que não temos esse item no momento, e sugira a alternativa mais próxima disponível.
        3. Se o produto ESTIVER no catálogo, apresente as opções de forma natural e agradável.
        NUNCA insista ou force a venda de um produto se o cliente pediu algo que não temos."""
        
        atualizar_etapa(telefone, "produto")

    else:
        # Fallback ou etapas futuras
        objetivo_etapa = "Responda à solicitação do cliente de forma útil e educada para continuar o atendimento."
        contexto_produtos = montar_contexto(mensagem) # Garante que a IA tenha contexto se perguntarem de preço

    # 3. Montar o Prompt Dinâmico
    prompt_final = f"""
    {instrucoes_base}

    [SUA MISSÃO ATUAL]
    {objetivo_etapa}

    [CATÁLOGO DISPONÍVEL NA LOJA]
    {contexto_produtos if contexto_produtos else 'Nenhum produto específico listado no momento.'}

    [MENSAGEM DO CLIENTE]
    {mensagem}
    """

   # 4. Executar com dupla proteção (Try/Except + Radar de Texto)
    try:
        resposta_ia = agent.run(prompt_final).content
        
        # O Radar: Se a IA devolver um texto que parece um código de erro JSON
        if '"error":' in resposta_ia and '"code":' in resposta_ia:
            print(f"⚠️ Erro silencioso da API capturado: {resposta_ia}")
            return "Poxa, o sistema da nossa lojinha deu uma pequena travada! 😅 Pode repetir o que você disse, por favor?"
            
        return resposta_ia
        
    except Exception as erro_api:
        print(f"⚠️ Erro crítico na IA: {erro_api}")
        return "Poxa, nossa lojinha está bem movimentada agora e eu acabei me perdendo! 😅 Você pode repetir o que disse, por favor?"