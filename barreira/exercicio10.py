import threading
import time
import random

NUM_CORREDORES = 6

class Corredor:
    def __init__(self, id_corredor, nome):
        self.id = id_corredor
        self.nome = nome
        self.tempo_final = None
        self.posicao = None

def competir(barreira, corredor, resultados, lock_resultados):
    """
    Simula um corredor que se prepara para a largada e,
    após todos estarem prontos, inicia a corrida.
    """
    # Chegando ao local da corrida
    print(f"🏃 Corredor #{corredor.id} ({corredor.nome}) chegou ao local da competição.")
    
    tempo_preparacao = random.uniform(1, 5)
    time.sleep(tempo_preparacao)
    
    print(f"👟 Corredor #{corredor.id} ({corredor.nome}) está pronto na linha de partida após {tempo_preparacao:.1f} segundos.")
    
    # Espera na linha de partida até que todos estejam prontos
    print(f"⏳ Corredor #{corredor.id} aguardando o sinal de largada...")
    barreira.wait()
    
    # O sinal de largada foi dado
    print(f"🏁 Vai! Corredor #{corredor.id} ({corredor.nome}) iniciou a corrida!")
    
    # Simula o tempo de corrida
    distancia = 100  
    velocidade = random.uniform(8, 12)  
    tempo_corrida = distancia / velocidade
    
    # Simula a corrida
    time.sleep(tempo_corrida)
    
    # Registra o tempo final
    corredor.tempo_final = tempo_corrida
    
    print(f"🏁 Corredor #{corredor.id} ({corredor.nome}) completou a corrida em {tempo_corrida:.2f} segundos!")
    
    # Adiciona aos resultados de forma thread-safe
    with lock_resultados:
        resultados.append(corredor)

def main():
    # Cria uma barreira para sincronizar todos os corredores na largada
    barreira = threading.Barrier(NUM_CORREDORES)
    
    # Lock para proteger a lista de resultados
    lock_resultados = threading.Lock()
    resultados = []
    
    # Nomes fictícios para os corredores
    nomes = ["Bolt", "Mateus", "Lucas", "Joao", "Gabriel", "Filipe", 
             "Bruno", "Marcos", "Marcell", "José", "Daniel", "Nathan"]
    
    # Cria objetos para cada corredor
    corredores = []
    for i in range(NUM_CORREDORES):
        corredores.append(Corredor(i+1, random.choice(nomes)))
    
    # Cria e inicia as threads
    threads = []
    print(f"🏆 Competição de corrida com {NUM_CORREDORES} atletas vai começar!")
    
    for corredor in corredores:
        t = threading.Thread(target=competir, args=(barreira, corredor, resultados, lock_resultados))
        threads.append(t)
        t.start()
        
        # Pequeno intervalo entre chegadas
        time.sleep(random.uniform(0.1, 0.5))
    
    # Espera todos os corredores terminarem
    for t in threads:
        t.join()
    
    # Classifica os resultados pelo tempo
    resultados.sort(key=lambda c: c.tempo_final)
    
    # Atribui as posições
    for i, corredor in enumerate(resultados):
        corredor.posicao = i + 1
    
    print("\n🏆 RESULTADOS DA CORRIDA 🏆")
    print("=" * 40)
    print("Pos. | Corredor | Tempo (s)")
    print("-" * 40)
    for corredor in resultados:
        print(f"{corredor.posicao:3d}  | #{corredor.id} {corredor.nome:<7} | {corredor.tempo_final:.2f}")
    print("=" * 40)
    
    print(f"🥇 CAMPEÃO: Corredor #{resultados[0].id} ({resultados[0].nome}) com {resultados[0].tempo_final:.2f} segundos!")

if __name__ == "__main__":
    main()

