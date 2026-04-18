from search import buscar_produtos

def montar_contexto(pergunta):
    produtos = buscar_produtos(pergunta)

    contexto = "Produtos disponíveis:\n"

    for p in produtos:
        # Formata o preço para ter duas casas decimais (ex: R$2.50)
        contexto += f"- {p['nome']} por R${p['preco']:.2f}\n"

    return contexto