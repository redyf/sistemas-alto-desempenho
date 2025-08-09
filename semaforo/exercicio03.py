import threading
import time
import random

# Criando o semáforo com capacidade para 3 carros
ponte_semaforo = threading.Semaphore(3)

# Total de carros que querem atravessar a ponte
NUM_CARROS = 10

def carro(id_carro):
    print(f"🚗 Carro {id_carro} chegou à ponte e está esperando para atravessar...")
    
    # Tenta adquirir acesso à ponte
    ponte_semaforo.acquire()
    
    try:
        print(f"🌉 Carro {id_carro} está atravessando a ponte...")
        # Simula o tempo de travessia (entre 1 e 3 segundos)
        tempo_travessia = random.uniform(1, 3)
        time.sleep(tempo_travessia)
        print(f"✅ Carro {id_carro} terminou de atravessar a ponte após {tempo_travessia:.1f} segundos.")
    finally:
        # Libera o acesso à ponte
        ponte_semaforo.release()

if __name__ == "__main__":
    # Lista para armazenar todas as threads
    threads = []
    
    # Cria as threads para cada carro
    for i in range(NUM_CARROS):
        t = threading.Thread(target=carro, args=(i+1,))
        threads.append(t)
        
        # Inicia a thread com um pequeno atraso aleatório
        t.start()
        time.sleep(random.uniform(0.1, 0.5))
    
    # Aguarda todas as threads terminarem
    for t in threads:
        t.join()
    
    print("🏁 Todos os carros atravessaram a ponte com sucesso!")

