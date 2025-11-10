import requests

# URLs base dos serviços (conforme exposto no docker-compose.yml)
URL_GERENCIAMENTO = "http://localhost:8081/api"
URL_ATIVIDADES = "http://localhost:8082/api"
URL_RESERVAS = "http://localhost:8083/api"

def seed_data():
    """
    Popula os bancos de dados dos microsserviços com dados de exemplo.
    """
    print("Iniciando o seeding dos bancos de dados...")

    try:
        # --- 1. Criar Professor (no Gerenciamento) ---
        print("\n[PASSO 1] Criando Professor...")
        prof_data = {
            "nome": "Ana Lucia",
            "idade": 45,
            "materia": "Banco de Dados"
        }
        response = requests.post(f"{URL_GERENCIAMENTO}/professores", json=prof_data)
        
        if response.status_code != 201:
            raise Exception(f"Erro ao criar professor: {response.text}")
            
        professor_criado = response.json()
        prof_id = professor_criado['id']
        print(f"-> Sucesso! Professor 'Ana Lucia' criado com ID: {prof_id}")

        # --- 2. Criar Turma (no Gerenciamento) ---
        print("\n[PASSO 2] Criando Turma...")
        turma_data = {
            "descricao": "Engenharia de Software - 2025",
            "ativo": True,
            "professor_id": prof_id  # <-- Usando o ID do passo anterior
        }
        response = requests.post(f"{URL_GERENCIAMENTO}/turmas", json=turma_data)
        
        if response.status_code != 201:
            raise Exception(f"Erro ao criar turma: {response.text}")

        turma_criada = response.json()
        turma_id = turma_criada['id']
        print(f"-> Sucesso! Turma 'Engenharia de Software - 2025' criada com ID: {turma_id}")

        # --- 3. Criar Aluno (no Gerenciamento) ---
        print("\n[PASSO 3] Criando Aluno...")
        aluno_data = {
            "nome": "Bruno Silva",
            "idade": 21,
            "data_nascimento": "15/05/2004",
            "nota_1_semestre": 8.0,
            "nota_2_semestre": 7.5,
            "turma_id": turma_id  # <-- Usando o ID do passo anterior
        }
        response = requests.post(f"{URL_GERENCIAMENTO}/alunos", json=aluno_data)

        if response.status_code != 201:
            raise Exception(f"Erro ao criar aluno: {response.text}")
        
        print(f"-> Sucesso! Aluno 'Bruno Silva' criado com ID: {response.json()['id']}")

        # --- 4. Criar Reserva (no Reservas) ---
        print("\n[PASSO 4] Criando Reserva...")
        reserva_data = {
            "num_sala": 303,
            "lab": False,
            "data_reserva": "20/12/2025",
            "turma_id": turma_id  # <-- Usando o ID da turma
        }
        # Note a URL diferente!
        response = requests.post(f"{URL_RESERVAS}/reservas", json=reserva_data) 
        
        if response.status_code != 201:
            raise Exception(f"Erro ao criar reserva: {response.text}")

        print(f"-> Sucesso! Reserva para sala 303 criada com ID: {response.json()['id']}")

        print("\nSeeding concluído com sucesso!")

    except requests.exceptions.ConnectionError as e:
        print("\n[ERRO FATAL] Não foi possível conectar aos serviços.")
        print("Certifique-se de que os containers do Docker estão rodando (`docker-compose up`).")
    except Exception as e:
        print(f"\n[ERRO DURANTE O SEEDING] {e}")

if __name__ == "__main__":
    seed_data()