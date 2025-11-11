import requests
import random

URL_GERENCIAMENTO = "http://localhost:8081/api"
URL_ATIVIDADES = "http://localhost:8082/api" 
URL_RESERVAS = "http://localhost:8083/api"   

def seed_data():
    """
    Popula os bancos de dados dos microsserviços com dados de exemplo.
    """
    print("Iniciando o seeding dos bancos de dados...")

    ids_professores = []
    ids_turmas = []
    ids_alunos = []
    ids_atividades = []

    try:
        # criar professores :)
        print("\n[PASSO 1] Criando Professores...")
        
        professores_para_criar = [
            {"nome": "Carlos Alberto", "idade": 42, "materia": "Engenharia de Software"},
            {"nome": "Ana Lucia", "idade": 45, "materia": "Banco de Dados"},
            {"nome": "Marcos Vinicius", "idade": 38, "materia": "Redes de Computadores"}
        ]

        for prof_data in professores_para_criar:
            response = requests.post(f"{URL_GERENCIAMENTO}/professores", json=prof_data)

            if response.status_code != 201:
                print(f"ERRO ao criar professor '{prof_data['nome']}': {response.text}")
                continue

            professor_criado = response.json()
            prof_id = professor_criado['id']

            ids_professores.append(prof_id)
        
            print(f"-> Sucesso! Professor '{professor_criado['nome']}' criado com ID: {prof_id}")

        if not ids_professores:
            raise Exception("Nenhum professor foi criado. Abortando o seeding.")

        # criar turma
        print("\n[PASSO 2] Criando 1 Turma...")
        turma_data = {
            "descricao": "Engenharia de Software - 2025",
            "ativo": True,
            "professor_id": ids_professores[0] 
        }
        response = requests.post(f"{URL_GERENCIAMENTO}/turmas", json=turma_data)
        
        if response.status_code != 201:
            raise Exception(f"Erro ao criar turma: {response.text}")

        turma_criada = response.json()
        turma_id_criada = turma_criada['id']
        ids_turmas.append(turma_id_criada)
        print(f"-> Sucesso! Turma '{turma_criada['descricao']}' criada com ID: {turma_id_criada}")

        # criar alunos 
        print("\n[PASSO 3] Criando 10 Alunos...")
        nomes = ["Ana", "Bruno", "Carla", "Cauan", "Isaac", "Felipe", "Gabriela", "Leonardo", "Isabela", "Joaquim"]
        for i in range(10):
            aluno_data = {
                "nome": f"{nomes[i]} {(i+1) * 100}",
                "idade": 20 + i,
                "data_nascimento": f"{10+i}/01/2004",
                "nota_1_semestre": round(random.uniform(5.0, 9.0), 1),
                "nota_2_semestre": round(random.uniform(6.0, 10.0), 1),
                "turma_id": turma_id_criada
            }
            response = requests.post(f"{URL_GERENCIAMENTO}/alunos", json=aluno_data)

            if response.status_code != 201:
                print(f"ERRO ao criar aluno '{aluno_data['nome']}': {response.text}")
                continue
            
            aluno_criado = response.json()
            aluno_id = aluno_criado['id']
            ids_alunos.append(aluno_id)
            print(f"-> Sucesso! Aluno '{aluno_criado['nome']}' criado com ID: {aluno_id}")

        # criar reservas
        print("\n[PASSO 4] Criando 3 Reservas...")
        reservas_para_criar = [
            {"num_sala": 101, "lab": False, "data_reserva": "25/11/2025", "turma_id": turma_id_criada},
            {"num_sala": 303, "lab": True, "data_reserva": "26/11/2025", "turma_id": turma_id_criada},
            {"num_sala": 101, "lab": False, "data_reserva": "27/11/2025", "turma_id": turma_id_criada}
        ]

        for reserva_data in reservas_para_criar:
            response = requests.post(f"{URL_RESERVAS}/reservas", json=reserva_data)
            
            if response.status_code != 201:
                print(f"ERRO ao criar reserva para sala '{reserva_data['num_sala']}': {response.text}")
                continue
            
            reserva_criada = response.json()
            print(f"-> Sucesso! Reserva para sala '{reserva_criada['num_sala']}' criada com ID: {reserva_criada['id']}")

        # criar atividades 
        print("\n[PASSO 5] Criando 2 Atividades...")
        atividades_para_criar = [
            {
                "nome_atividade": "AP1 - Microsserviços", "descricao": "Primeira entrega do projeto",
                "peso_porcento": 40, "data_entrega": "20/11/2025",
                "turma_id": turma_id_criada, "professor_id": ids_professores[0]
            },
            {
                "nome_atividade": "AP2 - Testes", "descricao": "Entrega final com testes de integração",
                "peso_porcento": 60, "data_entrega": "10/12/2025",
                "turma_id": turma_id_criada, "professor_id": ids_professores[0]
            }
        ]

        for atv_data in atividades_para_criar:
            response = requests.post(f"{URL_ATIVIDADES}/atividades", json=atv_data)
            
            if response.status_code != 201:
                print(f"ERRO ao criar atividade '{atv_data['nome_atividade']}': {response.text}")
                continue
            
            atividade_criada = response.json()
            atv_id = atividade_criada['id']
            ids_atividades.append(atv_id)
            print(f"-> Sucesso! Atividade '{atividade_criada['nome_atividade']}' criada com ID: {atv_id}")
        
        # criar notas 
        print("\n[PASSO 6] Criando 10 Notas...")
        if not ids_alunos or not ids_atividades:
            print("-> ERRO: Sem alunos ou atividades para criar notas. Pulando.")
        else:
            atividade_para_notas = ids_atividades[0] # Lança notas para a primeira atividade (AP1)

            for aluno_id in ids_alunos:
                nota_data = {
                    "nota_atividade": round(random.uniform(5.0, 10.0), 1),
                    "aluno_id": aluno_id,
                    "atividade_id": atividade_para_notas
                }
                response = requests.post(f"{URL_ATIVIDADES}/notas", json=nota_data)
                
                if response.status_code != 201:
                    print(f"ERRO ao criar nota para aluno '{aluno_id}': {response.text}")
                    continue
                
                print(f"-> Sucesso! Nota para Aluno ID {aluno_id} criada.")

        print("\n--- [ SEEDING CONCLUÍDO ] ---")

    except requests.exceptions.ConnectionError as e:
        print("\n[ERRO FATAL] Não foi possível conectar aos serviços.")
        print("Certifique-se de que os containers do Docker estão rodando (`docker-compose up`).")
    except Exception as e:
        print(f"\n[ERRO DURANTE O SEEDING] {e}")

if __name__ == "__main__":
    seed_data()