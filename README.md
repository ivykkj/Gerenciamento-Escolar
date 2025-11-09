# Ecossistema de Microsserviços de Gestão Escolar

Bem-vindo ao Ecossistema de Gestão Escolar\! Este projeto implementa uma arquitetura de microsserviços para gerenciar as operações de uma instituição de ensino, separando as responsabilidades em domínios de negócio distintos.

O ecossistema é composto por três serviços independentes:

  * **Serviço de Gerenciamento:** Responsável por Professores, Turmas e Alunos.
  * **Serviço de Reservas:** Responsável pelo agendamento e reserva de salas.
  * **Serviço de Atividades:** Responsável pelo gerenciamento de atividades e notas.

Cada serviço é uma API Flask completa, com seu próprio banco de dados, e todos são orquestrados usando Docker Compose.

-----

## Integrantes - Grupo 9

- Cauan de Melo Silva
- Leonardo Borges Soares
- Isaac do Nascimento Silva

-----

## Tecnologias Utilizadas

  * **Linguagem:** Python
  * **Framework:** Flask
  * **Comunicação API:** Flask-Cors, Requests
  * **Banco de Dados:** SQLite
  * **ORM:** Flask-SQLAlchemy
  * **Documentação:** Flasgger (Swagger UI)
  * **Containerização:** Docker
  * **Orquestração:** Docker Compose

-----

## 🚀 Instruções de Execução (com Docker)

A execução do projeto é gerenciada inteiramente pelo Docker Compose, que irá construir e iniciar os três microsserviços e a rede necessária para que eles se comuniquem.

**Pré-requisito:** Ter o **Docker Desktop** instalado em sua máquina.

**Passo 1: Construir as imagens dos 3 serviços**
No diretório raiz do projeto (onde está o `docker-compose.yml`), execute:

```bash
docker-compose build
```

**Passo 2: Iniciar o ecossistema completo**
Após o build, inicie todos os serviços:

```bash
docker-compose up
```

*(Você pode adicionar a flag `-d` para rodar em segundo plano).*

### Acesso aos Serviços

Após os serviços subirem, eles estarão acessíveis nas seguintes portas em sua máquina local:

  * **Gerenciamento (Alunos, Professores, Turmas):**

      * **API:** `http://localhost:8081`
      * **Documentação:** `http://localhost:8081/apidocs`

  * **Reservas (Reservas de Sala):**

      * **API:** `http://localhost:8082`
      * **Documentação:** `http://localhost:8082/apidocs`

  * **Atividades (Atividades e Notas):**

      * **API:** `http://localhost:8083`
      * **Documentação:** `http://localhost:8083/apidocs`

-----

## 🏛️ Explicação da Arquitetura Utilizada

Este projeto utiliza uma **Arquitetura de Microsserviços** .

  * **Microsserviços:** Em vez de uma única aplicação monolítica, o sistema é dividido em três serviços menores, independentes e focados em um único **Domínio de Negócio** (Gerenciamento, Reservas, Atividades).
  * **Monorepo:** Todos os serviços residem no mesmo repositório Git, o que facilita o gerenciamento, mas cada serviço é mantido em sua própria pasta e é totalmente desacoplado dos outros.
  * **Bancos de Dados Independentes:** Cada microsserviço possui seu próprio banco de dados SQLite (`database.db`). Isso reforça o **Encapsulamento de Domínio** e garante que cada serviço seja a única **Fonte da Verdade** para seus dados (ex: só o serviço de Gerenciamento pode escrever na tabela de Turmas).
  * **Orquestração com Docker Compose:** O `docker-compose.yml` é o "maestro" do sistema. Ele define os serviços, constrói suas imagens, e mais importante, cria uma **rede virtual (bridge)**. Dentro dessa rede, os serviços podem se comunicar usando seus nomes (ex: `http://gerenciamento-svc:8080`), o que é gerenciado pelo DNS interno do Docker.

-----

## 🌐 Ecossistema e Integração entre Serviços

A coesão do sistema é mantida através de **Comunicação Síncrona (HTTP)**. Os serviços "dependentes" (Reservas e Atividades) validam a existência de dados fazendo chamadas de API para o serviço "Fonte da Verdade" (Gerenciamento).

  * **Gerenciamento (Fonte da Verdade):**

      * **Porta:** `8081`
      * **Responsabilidade:** Gerencia o CRUD de Alunos, Professores e Turmas.
      * **Integração:** Nenhuma. Ele é a fonte da verdade e não conhece a existência dos outros serviços.

  * **Reservas (Serviço Dependente):**

      * **Porta:** `8082`
      * **Responsabilidade:** Gerencia o CRUD de Reservas de Sala.
      * **Integração:** Antes de `CRIAR` (POST) ou `ATUALIZAR` (PUT) uma Reserva, este serviço **pausa** sua execução e faz uma chamada `requests.get()` para o serviço de Gerenciamento (ex: `http://gerenciamento-svc:8080/api/turmas/{id}`) para validar se o `turma_id` fornecido realmente existe. Se receber um `404`, a operação é cancelada e um erro é retornado ao cliente.

  * **Atividades (Serviço Dependente):**

      * **Porta:** `8083`
      * **Responsabilidade:** Gerencia o CRUD de Atividades e Notas.
      * **Integração:** Segue a mesma lógica. Para `CRIAR` uma Atividade, ele valida o `turma_id` e o `professor_id` contra o serviço de Gerenciamento. Para `CRIAR` uma Nota, ele valida o `aluno_id` (no Gerenciamento) e o `atividade_id` (em seu próprio banco de dados).

-----

## 📋 Exemplos de Uso com cURL

**Atenção:** Note que cada `curl` aponta para uma porta diferente (`8081`, `8082` ou `8083`), dependendo do recurso que está sendo acessado.

### 👨‍🏫 Gerenciamento (Professores) - Porta 8081

**1. Criando um novo professor:**

```bash
curl -X POST http://localhost:8081/api/professores \
-H "Content-Type: application/json" \
-d '{
  "nome": "Carlos Alberto",
  "idade": 42,
  "materia": "Engenharia de Software"
}'
```

**2. Listando todos os professores:**

```bash
curl http://localhost:8081/api/professores
```

### 🏫 Gerenciamento (Turmas) - Porta 8081

**1. Criando uma nova turma (assume que o professor ID 1 existe):**

```bash
curl -X POST http://localhost:8081/api/turmas \
-H "Content-Type: application/json" \
-d '{
  "descricao": "Análise e Desenv. de Sistemas - Noite",
  "professor_id": 1
}'
```

**2. Listando todas as turmas:**

```bash
curl http://localhost:8081/api/turmas
```

### 🎓 Gerenciamento (Alunos) - Porta 8081

**1. Criando um novo aluno (assume que a turma ID 1 existe):**

```bash
curl -X POST http://localhost:8081/api/alunos \
-H "Content-Type: application/json" \
-d '{
  "nome": "Cauan Melo",
  "idade": 19,
  "data_nascimento": "25/02/2006",
  "nota_1_semestre": 8.5,
  "nota_2_semestre": 9.0,
  "turma_id": 1
}'
```

**2. Listando todos os alunos:**

```bash
curl http://localhost:8081/api/alunos
```

-----

### 📅 Reservas - Porta 8082

**1. Criando uma nova reserva (assume que a turma ID 1 existe):**

```bash
curl -X POST http://localhost:8082/api/reservas \
-H "Content-Type: application/json" \
-d '{
  "num_sala": 401,
  "lab": true,
  "data_reserva": "25/10/2025",
  "turma_id": 1
}'
```

**2. Listando todas as reservas:**

```bash
curl http://localhost:8082/api/reservas
```

-----

### 📝 Atividades e Notas - Porta 8083

**1. Criando uma nova atividade (assume que turma 1 e prof. 1 existem):**

```bash
curl -X POST http://localhost:8083/api/atividades \
-H "Content-Type: application/json" \
-d '{
  "nome_atividade": "Entrega AP2 - Microsserviços",
  "descricao": "Entrega final do projeto",
  "peso_porcento": 25,
  "data_entrega": "30/11/2025",
  "turma_id": 1,
  "professor_id": 1
}'
```

**2. Listando todas as atividades:**

```bash
curl http://localhost:8083/api/atividades
```

**3. Lançando uma nota (assume que aluno 1 e atividade 1 existem):**

```bash
curl -X POST http://localhost:8083/api/notas \
-H "Content-Type: application/json" \
-d '{
  "nota_atividade": 9.5,
  "aluno_id": 1,
  "atividade_id": 1
}'
```

**4. Listando todas as notas:**

```bash
curl http://localhost:8083/api/notas
```
