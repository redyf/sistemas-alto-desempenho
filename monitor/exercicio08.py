import threading
import time
import random

class UTI:
    def __init__(self):
        self.leito_ocupado = False
        self.lock = threading.Lock()
        self.leito_disponivel = threading.Condition(self.lock)
        self.paciente_atual = None
        print("🏥 UTI iniciada com 1 leito disponível.")
    
    def internar_paciente(self, id_paciente, gravidade):
        with self.lock:
            print(f"🚑 Paciente {id_paciente} (Gravidade: {gravidade}) chegou precisando de internação na UTI.")
            
            # Espera até que o leito esteja disponível
            while self.leito_ocupado:
                print(f"⏳ Paciente {id_paciente} está aguardando o leito da UTI ficar disponível...")
                self.leito_disponivel.wait()
            
            # Ocupa o leito
            self.leito_ocupado = True
            self.paciente_atual = id_paciente
            print(f"🛏️ Paciente {id_paciente} foi internado na UTI!")
    
    def liberar_paciente(self, id_paciente):
        with self.lock:
            # Verifica se é o paciente correto
            if self.paciente_atual != id_paciente:
                print(f"⚠️ Erro: Tentativa de liberar paciente incorreto {id_paciente}!")
                return
            
            # Libera o leito
            self.leito_ocupado = False
            self.paciente_atual = None
            print(f"🔄 Paciente {id_paciente} recebeu alta da UTI. Leito agora disponível.")
            
            # Notifica o próximo paciente
            self.leito_disponivel.notify()

def paciente(id_paciente, uti):
    try:
        # Gravidade do caso (1 a 10)
        gravidade = random.randint(7, 10)
        
        # Tenta internar na UTI
        uti.internar_paciente(id_paciente, gravidade)
        
        # Simula o tempo de tratamento baseado na gravidade
        tempo_tratamento = gravidade * random.uniform(0.5, 1.0)
        print(f"🏥 Paciente {id_paciente} está recebendo tratamento na UTI...")
        time.sleep(tempo_tratamento)
        
        # Estado após tratamento
        melhora = random.randint(1, 10)
        
        if melhora >= 7:
            print(f"😊 Paciente {id_paciente} melhorou significativamente após {tempo_tratamento:.1f} segundos.")
        else:
            print(f"😐 Paciente {id_paciente} teve leve melhora após {tempo_tratamento:.1f} segundos.")
        
        # Libera o leito
        uti.liberar_paciente(id_paciente)
        print(f"🚶 Paciente {id_paciente} foi transferido para enfermaria regular.")
    except Exception as e:
        print(f"⚠️ Erro com o paciente {id_paciente}: {e}")

if __name__ == "__main__":
    # Configuração
    TOTAL_PACIENTES = 5
    
    # Cria a UTI
    uti = UTI()
    
    # Lista para armazenar todas as threads
    threads = []
    
    # Cria e inicia as threads
    for i in range(TOTAL_PACIENTES):
        t = threading.Thread(target=paciente, args=(i+1, uti))
        threads.append(t)
        t.start()
        
        # Intervalo entre chegadas de pacientes
        time.sleep(random.uniform(0.5, 2.0))
    
    # Aguarda todas as threads terminarem
    for t in threads:
        t.join()
    
    print("🏁 Todos os pacientes foram atendidos na UTI.")
    if not uti.leito_ocupado:
        print("✅ UTI vazia e disponível para novos pacientes.")
    else:
        print(f"⚠️ UTI ainda ocupada pelo paciente {uti.paciente_atual}.")

