import threading
import time
import random

# Semáforo binário (mutex) para o caixa eletrônico
caixa_semaforo = threading.Semaphore(1)  # Apenas 1 pessoa por vez

# Número de clientes
NUM_CLIENTES = 6

# Saldo na conta (recurso compartilhado)
saldo = 1000
saldo_lock = threading.Lock()  # Lock adicional para proteger a variável de saldo

# Operações possíveis no caixa
OPERACOES = ["saque", "depósito", "consulta", "transferência"]

def usar_caixa_eletronico(id_cliente):
    global saldo
    
    # Escolhe uma operação aleatória
    operacao = random.choice(OPERACOES)
    valor = random.randint(10, 200) if operacao != "consulta" else 0
    
    print(f"👤 Cliente {id_cliente} chegou ao caixa para fazer um {operacao}...")
    
    # Tenta acessar o caixa eletrônico
    print(f"⏳ Cliente {id_cliente} está aguardando na fila...")
    caixa_semaforo.acquire()
    
    try:
        print(f"🏧 Cliente {id_cliente} está acessando o caixa eletrônico...")
        
        # Simula o tempo da operação (entre 2 e 5 segundos)
        tempo_operacao = random.uniform(2, 5)
        time.sleep(tempo_operacao)
        
        # Realiza a operação no saldo
        with saldo_lock:
            if operacao == "saque":
                if saldo >= valor:
                    saldo -= valor
                    print(f"💰 Cliente {id_cliente} sacou R${valor:.2f}. Saldo atual: R${saldo:.2f}")
                else:
                    print(f"❌ Cliente {id_cliente} tentou sacar R${valor:.2f}, mas não há saldo suficiente.")
            elif operacao == "depósito":
                saldo += valor
                print(f"💵 Cliente {id_cliente} depositou R${valor:.2f}. Saldo atual: R${saldo:.2f}")
            elif operacao == "consulta":
                print(f"📊 Cliente {id_cliente} consultou o saldo: R${saldo:.2f}")
            else:  # transferência
                if saldo >= valor:
                    saldo -= valor
                    print(f"📲 Cliente {id_cliente} transferiu R${valor:.2f}. Saldo atual: R${saldo:.2f}")
                else:
                    print(f"❌ Cliente {id_cliente} tentou transferir R${valor:.2f}, mas não há saldo suficiente.")
        
        print(f"✅ Cliente {id_cliente} finalizou sua operação após {tempo_operacao:.1f} segundos.")
    finally:
        # Libera o caixa eletrônico
        caixa_semaforo.release()

if __name__ == "__main__":
    # Lista para armazenar todas as threads
    threads = []
    
    print(f"🏦 O caixa eletrônico está aberto. Saldo inicial: R${saldo:.2f}")
    
    # Cria as threads para cada cliente
    for i in range(NUM_CLIENTES):
        t = threading.Thread(target=usar_caixa_eletronico, args=(i+1,))
        threads.append(t)
        
        # Inicia a thread com um pequeno intervalo entre chegadas
        t.start()
        time.sleep(random.uniform(0.5, 1.5))
    
    # Aguarda todas as threads terminarem
    for t in threads:
        t.join()
    
    print(f"🏁 O caixa eletrônico fechou. Saldo final: R${saldo:.2f}")

