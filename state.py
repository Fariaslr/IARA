estado_clientes = {}

def obter_estado(telefone):
    if telefone not in estado_clientes:
        estado_clientes[telefone] = {
            "etapa": "inicio",
            "carrinho": []
        }
    return estado_clientes[telefone]


def atualizar_etapa(telefone, nova_etapa):
    estado_clientes[telefone]["etapa"] = nova_etapa