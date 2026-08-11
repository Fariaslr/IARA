catalog_data = [
    {
        "name": "Bolsa de Crochê Maresia", 
        "category": "bolsas", 
        "price": 120.00, 
        "type": "sob encomenda", 
        "production_time": "7 dias úteis"
    },
    {
        "name": "Amigurumi Polvo", 
        "category": "pelucias", 
        "price": 45.00, 
        "type": "pronta-entrega", 
        "production_time": "envio imediato"
    },
    {
        "name": "Sousplat Clássico", 
        "category": "mesa posta", 
        "price": 35.00, 
        "type": "sob encomenda", 
        "production_time": "3 dias úteis por unidade"
    }
]

def get_catalog_context():
    """
    Formata o catálogo em um texto estruturado para injetar no prompt do LLM (RAG).
    Isso evita alucinações e garante que a IARA saiba preços e prazos exatos.
    """
    context = "Catálogo de Produtos - Maresia Crochê:\n\n"
    
    for item in catalog_data:
        preco_formatado = f"{item['price']:.2f}".replace('.', ',')
        
        context += f"- Produto: {item['name']}\n"
        context += f"  Categoria: {item['category']}\n"
        context += f"  Preço: R$ {preco_formatado}\n"
        context += f"  Disponibilidade: {item['type']}\n"
        context += f"  Prazo: {item['production_time']}\n\n"
        
    return context