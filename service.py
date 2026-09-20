from state import get_state, update_step, update_state_name, register_history
from database import save_customer
from catalog import get_catalog_context

def process_service(phone, message, agent):
    state = get_state(phone)
    current_step = state["step"]
    customer_name = state.get("name", "")

    # ETAPA 1: Boas-vindas iniciais
    if current_step == "coletar_nome":
        update_step(phone, "salvar_nome")
        return "Olá! 👋 Sou a IARA, assistente virtual do ateliê Maresia Crochê. Para eu te atender de forma mais personalizada, como você gostaria de ser chamado(a)?"

    # ETAPA 2: Salva o nome e faz o Call to Action para o Catálogo
    if current_step == "salvar_nome":
        name = message.strip()
        save_customer(phone, name)
        update_state_name(phone, name)
        update_step(phone, "inicio")
        return f"Muito prazer, {name}! 🥰 Nós trabalhamos com lindas bolsas de crochê, amigurumis e peças para mesa posta.\n\nVocê gostaria de dar uma olhada no nosso catálogo de produtos?"

    catalog_text = get_catalog_context()
    history_text = "\n".join(state["history"]) if state["history"] else "Nenhum histórico anterior."

    # INSTRUÇÕES BASE (Regras de UX e Verbosidade)
    base_instructions = f"""Você é a IARA, assistente virtual do ateliê Maresia Crochê.
    - REGRA DE FORMATAÇÃO: Seja EXTREMAMENTE concisa, direta e objetiva. 
    - Responda com mensagens curtas, ideais para leitura rápida na tela do WhatsApp.
    - NUNCA escreva parágrafos longos e não explique o que você está fazendo (apenas faça).
    - O nome do cliente com quem você está falando é {customer_name}. Chame-o pelo nome, mas evite repetir o nome em todas as mensagens.
    - Nunca prometa entregas imediatas para itens "sob encomenda".
    - Use no máximo 1 emoji por frase.
    """

    step_objective = ""

    # MÁQUINA DE ESTADOS
    if current_step == "inicio":
        step_objective = """O cliente respondeu positivamente e quer ver o catálogo. 
        Liste todos os produtos do [CATÁLOGO DISPONÍVEL] com seus preços de forma estruturada. 
        Ao final, pergunte qual dos itens mais chamou a atenção dele."""
        update_step(phone, "produto")
        
    elif current_step == "produto":
        step_objective = """O cliente está buscando produtos ou escolhendo itens.
        REGRA 1: NUNCA repita boas-vindas se você já o cumprimentou. Vá direto ao assunto.
        REGRA 2: Baseie-se APENAS no [CATÁLOGO DISPONÍVEL]. Informe prazos se for sob encomenda.
        REGRA 3: Se o cliente escolheu quantidades, CALCULE O VALOR TOTAL (preço unitário x quantidade) e pergunte se ele quer finalizar o pedido ou adicionar mais algo."""
        
        # Analisa a intenção da mensagem para avançar o funil
        mensagem_min = message.lower()
        palavras_chave = ["só isso", "fechar", "finalizar", "sim", "pode", "quero"]
        
        if any(palavra in mensagem_min for palavra in palavras_chave):
            update_step(phone, "carrinho")
            
    elif current_step == "carrinho":
        step_objective = """O cliente está no caixa para finalizar a compra e realizar o pagamento.
        REGRA 1: É ESTRITAMENTE PROIBIDO encerrar o atendimento, confirmar o pedido final ou se despedir antes de receber o pagamento.
        REGRA 2: Se a forma de pagamento ainda não foi escolhida, pergunte ativamente: 'Qual será a forma de pagamento (Pix, Cartão ou Dinheiro)?'.
        REGRA 3: Se o cliente escolher PIX, envie a chave Celular (71) 99999-9999 em nome de Maresia Crochê."""
        
    else:
        step_objective = "Responda à solicitação do cliente de forma útil e educada para continuar o atendimento."

    # MONTAGEM FINAL DO PROMPT PARA O LLM
    final_prompt = f"""
    {base_instructions}

    [SUA MISSÃO ATUAL]
    {step_objective}

    [CATÁLOGO DISPONÍVEL NA LOJA]
    {catalog_text}

    [MEMÓRIA DA CONVERSA (HISTÓRICO)]
    {history_text}

    [MENSAGEM ATUAL DO CLIENTE]
    {message}
    """

    # CHAMADA DE API E TRATAMENTO DE ERROS
    try:
        ai_response = agent.run(final_prompt).content
        
        # Intercepta bloqueios por limite de API (Error 429) em JSON oculto
        if '"error":' in ai_response and '"code":' in ai_response:
            print(f"⚠️ Erro silencioso da API capturado: {ai_response}")
            return "Poxa, o sistema do nosso ateliê deu uma pequena travada! 😅 Pode repetir o que você disse, por favor?"
        
        register_history(phone, message, ai_response)
        
        print("\n" + "="*55)
        print(f"📜 HISTÓRICO EM MEMÓRIA (Cliente: {customer_name})")
        print("="*55)
        for linha_conversa in state["history"]:
            print(linha_conversa)
        print("="*55 + "\n")
        
        return ai_response
        
    except Exception as api_error:
        print(f"⚠️ Erro crítico na IA: {api_error}")
        return "Poxa, nosso ateliê está bem movimentado agora e eu acabei me perdendo! 😅 Você pode repetir o que disse, por favor?"