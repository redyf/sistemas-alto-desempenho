import threading
import time

# Variáveis de sincronização
mutex = threading.Lock()
cond = threading.Condition(mutex)
pedido_pronto = False

def cliente():
    global pedido_pronto
    
    print("👤 Cliente faz o pedido")
    
    with cond:
        while not pedido_pronto:
            print("👤 Cliente aguardando o pedido ficar pronto...")
            cond.wait()
        
        print("👤 Cliente recebeu e está consumindo o pedido! 😋")

def garcom():
    global pedido_pronto
    
    # Simula o tempo de preparação do pedido
    print("👨‍🍳 Garçom preparando o pedido...")
    time.sleep(3)
    
    with cond:
        pedido_pronto = True
        print("👨‍🍳 Garçom: Pedido está pronto!")
        cond.notify()

if __name__ == "__main__":
    # Criando as threads
    t_cliente = threading.Thread(target=cliente)
    t_garcom = threading.Thread(target=garcom)
    
    # Iniciando as threads
    t_cliente.start()
    t_garcom.start()
    
    # Aguardando a conclusão das threads
    t_cliente.join()
    t_garcom.join()
    
    print("Restaurante fechou por hoje!")

