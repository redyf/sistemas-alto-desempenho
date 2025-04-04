import threading
import time
import random

# Constantes
NUM_IMPRESSORAS = 3
NUM_USUARIOS = 8

# Semáforo para controlar acesso às impressoras
impressoras_semaforo = threading.Semaphore(NUM_IMPRESSORAS)

# Lock para evitar que mensagens de saída se misturem
print_lock = threading.Lock()

def imprimir_documento(id_usuario):
    nome_documento = f"Doc-{id_usuario}"
    
    with print_lock:
        print(f"📄 Usuário {id_usuario} enviou o documento '{nome_documento}' para impressão e está aguardando...")
    
    # Tenta obter acesso a uma impressora
    impressoras_semaforo.acquire()
    
    try:
        # Quando consegue uma impressora
        with print_lock:
            print(f"🖨️ Usuário {id_usuario} está imprimindo '{nome_documento}'...")
        
        # Simula o tempo de impressão (entre 1 e 4 segundos)
        tempo_impressao = random.uniform(1, 4)
        time.sleep(tempo_impressao)
        
        with print_lock:
            print(f"✅ Usuário {id_usuario} terminou de imprimir '{nome_documento}' após {tempo_impressao:.1f} segundos.")
    finally:
        # Libera a impressora para o próximo usuário
        impressoras_semaforo.release()

if __name__ == "__main__":
    # Lista para armazenar todas as threads
    threads = []
    
    print(f"🖨️ Sistema de impressão iniciado com {NUM_IMPRESSORAS} impressoras disponíveis.")
    
    # Cria as threads para cada usuário
    for i in range(NUM_USUARIOS):
        t = threading.Thread(target=imprimir_documento, args=(i+1,))
        threads.append(t)
        
        # Inicia a thread
        t.start()
        # Pequeno atraso entre os envios para simular chegada de diferentes usuários
        time.sleep(random.uniform(0.1, 0.7))
    
    # Aguarda todas as threads terminarem
    for t in threads:
        t.join()
    
    print("🏁 Todos os documentos foram impressos com sucesso!")

