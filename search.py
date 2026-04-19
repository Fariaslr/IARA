from catalogo import catalogo

def buscar_produtos(pergunta):
    resultados = []
    
    if not pergunta:
        return catalogo

    pergunta = pergunta.lower()

    for produto in catalogo:
        if (
            produto["nome"].lower() in pergunta
            or produto["categoria"].lower() in pergunta
        ):
            resultados.append(produto)

    if not resultados:
        return catalogo

    return resultados