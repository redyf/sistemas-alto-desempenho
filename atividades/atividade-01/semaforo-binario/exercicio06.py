import threading
import time
import random

# Semáforo binário para acesso ao banco de dados
banco_dados_semaforo = threading.Semaphore(1)  # Apenas 1 usuário por vez pode modificar

# Lista de usuários (simulando o banco de dados de credenciais)
usuarios = {
    "admin": "admin123",
    "usuario1": "senha123",
    "usuario2": "abc123"
}

# Número de operações a serem realizadas
NUM_OPERACOES = 8

def operacao_credenciais(id_operacao):
    # Define aleatoriamente se é uma leitura ou modificação
    operacao_tipo = random.choice(["leitura", "modificacao"])
    
    if operacao_tipo == "leitura":
        # Leitura não precisa de exclusão mútua
        usuario = random.choice(list(usuarios.keys()))
        print(f"👀 Operação {id_operacao}: Lendo informações do usuário '{usuario}'...")
        
        # Simula tempo de leitura
        time.sleep(random.uniform(0.5, 1.5))
        
        print(f"📖 Operação {id_operacao}: Concluída leitura do usuário '{usuario}'")
    else:
        # Modificação precisa de exclusão mútua
        print(f"🔄 Operação {id_operacao}: Solicitando acesso para modificar o banco de dados...")
        
        # Tenta adquirir o semáforo para modificação
        banco_dados_semaforo.acquire()
        
        try:
            # Escolhe aleatoriamente uma operação de modificação
            mod_operacao = random.choice(["adicionar", "alterar", "remover"])
            
            if mod_operacao == "adicionar":
                novo_usuario = f"novo_usuario{random.randint(1, 100)}"
                nova_senha = f"senha{random.randint(100, 999)}"
                
                print(f"➕ Operação {id_operacao}: Adicionando usuário '{novo_usuario}'...")
                time.sleep(random.uniform(1, 2))
                
                usuarios[novo_usuario] = nova_senha
                print(f"✅ Operação {id_operacao}: Usuário '{novo_usuario}' adicionado com sucesso")
            
            elif mod_operacao == "alterar":
                if usuarios:
                    usuario = random.choice(list(usuarios.keys()))
                    nova_senha = f"nova_senha{random.randint(100, 999)}"
                    
                    print(f"🔄 Operação {id_operacao}: Alterando senha do usuário '{usuario}'...")
                    time.sleep(random.uniform(1, 2))
                    
                    usuarios[usuario] = nova_senha
                    print(f"✅ Operação {id_operacao}: Senha do usuário '{usuario}' alterada com sucesso")
            
            else:  # remover
                if len(usuarios) > 1:  # Mantém pelo menos um usuário
                    usuario = random.choice(list(usuarios.keys()))
                    
                    print(f"❌ Operação {id_operacao}: Removendo usuário '{usuario}'...")
                    time.sleep(random.uniform(1, 2))
                    
                    del usuarios[usuario]
                    print(f"✅ Operação {id_operacao}: Usuário '{usuario}' removido com sucesso")
                else:
                    print(f"⚠️ Operação {id_operacao}: Não é possível remover - mínimo de usuários atingido")
        finally:
            # Libera o semáforo
            banco_dados_semaforo.release()
            print(f"🔓 Operação {id_operacao}: Liberou o acesso ao banco de dados")

if __name__ == "__main__":
    # Lista para armazenar todas as threads
    threads = []
    
    print("🔐 Sistema de gerenciamento de credenciais iniciado")
    print(f"📊 Estado inicial do banco de dados: {len(usuarios)} usuários")
    
    # Cria as threads para cada operação
    for i in range(NUM_OPERACOES):
        t = threading.Thread(target=operacao_credenciais, args=(i+1,))
        threads.append(t)
        
        # Inicia a thread
        t.start()
        # Pequeno intervalo entre operações
        time.sleep(random.uniform(0.3, 0.8))
    
    # Aguarda todas as threads terminarem
    for t in threads:
        t.join()
    
    print("🏁 Todas as operações foram concluídas")
    print(f"📊 Estado final do banco de dados: {len(usuarios)} usuários")
    print(f"👥 Usuários atuais: {', '.join(usuarios.keys())}")

