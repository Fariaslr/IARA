from database import get_customer

customer_states = {}

def get_state(phone):
    """
    Inicializa ou recupera o estado transacional e a memória do cliente.
    """
    if phone not in customer_states:
        saved_name = get_customer(phone)
        
        customer_states[phone] = {
            "step": "inicio" if saved_name else "coletar_nome",
            "name": saved_name, 
            "cart": [],
            "history": [],
            "consecutive_errors": 0
        }
    return customer_states[phone]

def update_step(phone, new_step):
    customer_states[phone]["step"] = new_step

def update_state_name(phone, name):
    customer_states[phone]["name"] = name

def register_history(phone, customer_message, ai_response):
    """
    Mantém apenas as últimas 4 interações ativas na memória.
    """
    history = customer_states[phone]["history"]
    
    history.append(f"Cliente: {customer_message}")
    history.append(f"IARA: {ai_response}")
    
    if len(history) > 8:
        history.pop(0)
        history.pop(0)