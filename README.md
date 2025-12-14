# BarbearIA

Sistema de gerenciamento de barbearia. Projeto da disciplina "Métodos de Projeto de Software", prof. Raoni Kulesza

## 👥 Equipe

- Leudo Alves Pedrosa Neto - 20250158656
- Luiz Paulo de Souza Fontes Junior - 20230146291
- João Victor Martins Dantas - 20220070761
- João Vitor Cardoso Beltrão - 20220006134
- Artur Dartagnan de Oliveira Vasconcelos - 20210026643
- Ana Clara Ferreira Epaminondas - 20220006250

## 📚 Documentação

- **[Documentação da API](./backend/README.md)** - Endpoints, exemplos de uso e modelos de dados
- **[Diagramas UML](./docs/README.md)** - Casos de uso e diagramas de classes

## 🚀 Instalação e Execução

### Opção 1: Com Docker (Recomendado)

#### Pré-requisitos
- Docker
- Docker Compose

#### Passos

1. **Clone o repositório**
```bash
git clone https://github.com/LeudoNeto/BarbearIA.git
cd BarbearIA
```

2. **Configure as variáveis de ambiente**

Crie o arquivo `backend/.env` (ou copie o `.env.example`):
```bash
MYSQL_HOST=barbearia_mysql
MYSQL_PORT=3306
MYSQL_USER=barbearia_user
MYSQL_PASSWORD=sua_senha_segura
MYSQL_DATABASE=barbearia_db
```

3. **Inicie os containers**
```bash
docker compose up -d
```

4. **Aguarde a inicialização**

O MySQL pode levar alguns segundos para inicializar completamente. Aguarde até ver as mensagens de inicialização.

5. **Execute o schema do banco de dados**

```bash
docker exec -i barbearia_mysql mysql -u barbearia_user -p barbearia_db < backend/database_schema.sql
```

Quando solicitado, digite a senha configurada no `.env`.

6. **Acesse a aplicação**

- API: http://localhost:8000
- Documentação Swagger: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

#### Comandos Úteis

```bash
# Ver logs dos containers
docker compose logs -f

# Parar os containers
docker compose down

# Parar e remover volumes (limpa o banco de dados)
docker compose down -v

# Reconstruir as imagens
docker compose build

# Reiniciar apenas o backend
docker compose restart backend
```

### Opção 2: Instalação Local

#### Pré-requisitos
- Python 3.8+
- MySQL 8.0+
- pip

#### Passos

1. **Clone o repositório**
```bash
git clone https://github.com/LeudoNeto/BarbearIA.git
cd BarbearIA
```

2. **Instale as dependências**
```bash
cd backend
pip install -r requirements.txt
```

3. **Configure o banco de dados MySQL**

Execute o script SQL para criar o banco e tabelas:
```bash
mysql -u root -p < database_schema.sql
```

4. **Configure as variáveis de ambiente**

Crie o arquivo `backend/.env`:
```bash
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=sua_senha
MYSQL_DATABASE=barbearia_db
```

5. **Execute a aplicação**
```bash
python main.py
```

Ou usando uvicorn diretamente:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

6. **Acesse a aplicação**

- API: http://localhost:8000
- Documentação Swagger: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🛠️ Tecnologias

- **FastAPI**: Framework web moderno e rápido
- **PyMySQL**: Driver MySQL puro Python (sem ORM)
- **Python 3.11**: Linguagem de programação
- **MySQL 8.0**: Banco de dados relacional
- **Docker**: Containerização