import threading
import time
import random

# Variáveis de sincronização
mutex = threading.Lock()
cond = threading.Condition(mutex)
dados_prontos = False
dados = []

def gerador_dados():
    global dados_prontos, dados
    
    print("📊 Gerador: Iniciando geração de dados...")
    
    # Simulando processamento de dados
    time.sleep(2)
    
    # Gerando dados fictícios
    with cond:
        for i in range(5):
            dados.append(f"Dado {i+1}: {random.randint(100, 999)}")
        
        dados_prontos = True
        print("📊 Gerador: Dados concluídos e prontos para exibição!")
        cond.notify()

def exibidor_relatorio():
    global dados_prontos, dados
    
    with cond:
        while not dados_prontos:
            print("📋 Exibidor: Aguardando dados serem gerados...")
            cond.wait()
        
        print("\n📋 RELATÓRIO FINAL 📋")
        print("=" * 30)
        for dado in dados:
            print(dado)
        print("=" * 30)
        print("📋 Relatório exibido com sucesso!")

if __name__ == "__main__":
    # Criando as threads
    t_gerador = threading.Thread(target=gerador_dados)
    t_exibidor = threading.Thread(target=exibidor_relatorio)
    
    # Iniciando as threads
    t_exibidor.start()  # Iniciamos o exibidor primeiro para garantir que ele espere
    t_gerador.start()
    
    # Aguardando a conclusão das threads
    t_exibidor.join()
    t_gerador.join()
    
    print("Sistema de relatório finalizado!")

