import threading
import time
import random

NUM_AVENTUREIROS = 5

def aventureiro(barreira, id_aventureiro, habilidades):
    """
    Simula um aventureiro que precisa chegar ao ponto de encontro
    antes que o grupo possa atravessar a caverna.
    """
    print(f"🧙 Aventureiro {id_aventureiro} ({habilidades}) iniciou sua jornada.")
    
    # Simula o tempo de viagem até o ponto de encontro
    distancia = random.uniform(5, 15)
    velocidade = random.uniform(1, 3)
    tempo_viagem = distancia / velocidade
    
    print(f"🚶 Aventureiro {id_aventureiro} está viajando {distancia:.1f} km até o ponto de encontro...")
    time.sleep(tempo_viagem)
    
    print(f"🏁 Aventureiro {id_aventureiro} chegou ao ponto de encontro após {tempo_viagem:.1f} horas.")
    
    # Espera no ponto de encontro até que todos os aventureiros cheguem
    print(f"⏳ Aventureiro {id_aventureiro} está aguardando os outros aventureiros...")
    barreira.wait()
    
    print(f"🎉 Aventureiro {id_aventureiro} se juntou ao grupo completo!")
    
    # Atravessando a caverna juntos
    print(f"🔦 Aventureiro {id_aventureiro} está atravessando a caverna com o grupo.")
    
    # Simula o tempo de travessia da caverna
    tempo_travessia = random.uniform(2, 4)
    time.sleep(tempo_travessia)
    
    # Segunda barreira: espera todos saírem da caverna
    print(f"⏳ Aventureiro {id_aventureiro} chegou na saída e está esperando os outros...")
    barreira.wait()
    
    print(f"🌞 Aventureiro {id_aventureiro} saiu da caverna com sucesso após {tempo_travessia:.1f} horas!")

def main():
    # Cria uma barreira para sincronizar todos os aventureiros
    barreira = threading.Barrier(NUM_AVENTUREIROS)
    
    # Lista de habilidades possíveis
    habilidades_lista = ["Guerreiro", "Mago", "Arqueiro", "Clérigo", "Ladino", "Bardo", "Druida"]
    
    # Cria e inicia as threads para cada aventureiro
    threads = []
    print(f"🏰 Uma aventura começa com {NUM_AVENTUREIROS} aventureiros!")
    
    for i in range(NUM_AVENTUREIROS):
        # Seleciona uma habilidade aleatória para o aventureiro
        habilidade = random.choice(habilidades_lista)
        
        t = threading.Thread(target=aventureiro, args=(barreira, i+1, habilidade))
        threads.append(t)
        t.start()
        
        # Pequeno intervalo entre partidas
        time.sleep(random.uniform(0.2, 0.8))
    
    # Espera todos os aventureiros completarem a jornada
    for t in threads:
        t.join()
    
    print("🏆 Todos os aventureiros completaram a missão com sucesso!")

if __name__ == "__main__":
    main()

