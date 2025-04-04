import threading
import time
import random

class EstacaoBicicletas:
    def __init__(self, total_bicicletas):
        self.total_bicicletas = total_bicicletas
        self.bicicletas_disponiveis = total_bicicletas
        self.lock = threading.Lock()
        self.disponivel = threading.Condition(self.lock)
        print(f"🚲 Estação iniciada com {self.total_bicicletas} bicicletas disponíveis.")
    
    def alugar_bicicleta(self, id_pessoa):
        with self.lock:
            print(f"👤 Pessoa {id_pessoa} chegou para alugar uma bicicleta.")
            
            # Espera até que haja alguma bicicleta disponível
            while self.bicicletas_disponiveis == 0:
                print(f"⏳ Pessoa {id_pessoa} está aguardando uma bicicleta ficar disponível...")
                self.disponivel.wait()
            
            # Aluga a bicicleta
            self.bicicletas_disponiveis -= 1
            print(f"🚴 Pessoa {id_pessoa} alugou uma bicicleta! Restam {self.bicicletas_disponiveis} bicicletas.")
    
    def devolver_bicicleta(self, id_pessoa):
        with self.lock:
            # Devolve a bicicleta
            self.bicicletas_disponiveis += 1
            print(f"🔄 Pessoa {id_pessoa} devolveu a bicicleta. Agora há {self.bicicletas_disponiveis} bicicletas disponíveis.")
            
            # Notifica alguém que possa estar esperando
            self.disponivel.notify()

def usar_bicicleta(id_pessoa, estacao):
    try:
        # Tenta alugar uma bicicleta
        estacao.alugar_bicicleta(id_pessoa)
        
        # Simula o tempo de passeio
        tempo_passeio = random.uniform(2, 5)
        print(f"🚵 Pessoa {id_pessoa} está pedalando pela cidade...")
        time.sleep(tempo_passeio)
        
        # Devolve a bicicleta
        estacao.devolver_bicicleta(id_pessoa)
        print(f"✅ Pessoa {id_pessoa} concluiu o passeio após {tempo_passeio:.1f} segundos.")
    except Exception as e:
        print(f"⚠️ Erro com a pessoa {id_pessoa}: {e}")

if __name__ == "__main__":
    # Configuração
    TOTAL_BICICLETAS = 3
    TOTAL_PESSOAS = 8
    
    # Cria a estação de bicicletas
    estacao = EstacaoBicicletas(TOTAL_BICICLETAS)
    
    # Lista para armazenar todas as threads
    threads = []
    
    # Cria e inicia as threads
    for i in range(TOTAL_PESSOAS):
        t = threading.Thread(target=usar_bicicleta, args=(i+1, estacao))
        threads.append(t)
        t.start()
        
        # Pequeno intervalo entre chegadas
        time.sleep(random.uniform(0.3, 1.0))
    
    # Aguarda todas as threads terminarem
    for t in threads:
        t.join()
    
    print(f"🏁 Sistema de aluguel fechado. Bicicletas disponíveis: {estacao.bicicletas_disponiveis}/{TOTAL_BICICLETAS}")
