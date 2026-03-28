# BarbearIA - Documentação da API

API REST para gerenciamento de barbearia desenvolvida com FastAPI.

## 📋 Índice

- [URL Base](#url-base)
- [Endpoints](#endpoints)
  - [Autenticação](#autenticação)
  - [Clientes](#clientes)
  - [Funcionários](#funcionários)
  - [Empresa](#empresa)
  - [Horários de Funcionamento](#horários-de-funcionamento)
  - [Agendamentos](#agendamentos)
  - [Estatísticas](#estatísticas)
- [Modelos de Dados](#modelos-de-dados)
- [Respostas de Erro](#respostas-de-erro)

## URL Base

```
http://localhost:8000
```

## Endpoints

### Autenticação

#### Login

```http
POST /auth/login
```

**Corpo da Requisição:**

```json
{
  "email": "usuario@email.com",
  "senha": "senha123"
}
```

**Exemplo de Resposta (200 OK):**

```json
{
  "id": 1,
  "email": "usuario@email.com",
  "foto": null,
  "tipo": "cliente",
  "telefone": "84999887766"
}
```

> **Nota:** Define um cookie `session_id` HttpOnly com duração de 24 horas.

#### Cadastro (Signup)

```http
POST /auth/signup
```

**Corpo da Requisição:**

```json
{
  "email": "novocliente@email.com",
  "senha": "SenhaForte123!",
  "telefone": "84999887766",
  "foto": null
}
```

**Exemplo de Resposta (201 Created):**

```json
{
  "id": 5,
  "email": "novocliente@email.com",
  "telefone": "84999887766",
  "foto": null
}
```

#### Obter Usuário Logado

```http
GET /auth/me
```

**Requer:** Cookie `session_id`

**Exemplo de Resposta (200 OK):**

```json
{
  "id": 1,
  "email": "usuario@email.com",
  "foto": null,
  "tipo": "funcionario",
  "eh_barbeiro": true,
  "eh_admin": false
}
```

#### Logout

```http
POST /auth/logout
```

**Requer:** Cookie `session_id`

**Exemplo de Resposta (200 OK):**

```json
{
  "message": "Logout realizado com sucesso"
}
```

#### Obter RelatÃ³rio HTML de Acessos dos UsuÃ¡rios

```http
GET /estatisticas/acessos/relatorio-html
```

**Exemplo de Resposta (200 OK):**

```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <title>Relatorio de Acessos</title>
</head>
<body>
  <header>
    <h1>Relatorio de Acessos dos Usuarios</h1>
  </header>
  <section>
    <h2>Usuarios que acessaram</h2>
  </section>
</body>
</html>
```

> **Nota:** Retorna o relatÃ³rio de acessos em HTML renderizÃ¡vel no navegador, gerado com Template Method a partir das estatÃ­sticas consolidadas de login.

---

### Clientes

#### Listar Todos os Clientes

```http
GET /clientes
```

**Exemplo de Requisição:**

```bash
curl http://localhost:8000/clientes
```

**Exemplo de Resposta (200 OK):**

```json
[
  {
    "id": 1,
    "email": "joao@email.com",
    "telefone": "84999887766",
    "foto": null
  },
  {
    "id": 2,
    "email": "maria@email.com",
    "telefone": "84988776655",
    "foto": null
  }
]
```

#### Criar Novo Cliente

```http
POST /clientes
```

**Corpo da Requisição:**

```json
{
  "email": "cliente@email.com",
  "senha": "senha123",
  "telefone": "84999887766",
  "foto": null
}
```

**Exemplo de Requisição:**

```bash
curl -X POST http://localhost:8000/clientes \
  -H "Content-Type: application/json" \
  -d '{
    "email": "cliente@email.com",
    "senha": "senha123",
    "telefone": "84999887766"
  }'
```

**Exemplo de Resposta (201 Created):**

```json
{
  "id": 3,
  "email": "cliente@email.com",
  "telefone": "84999887766",
  "foto": null
}
```

---

### Funcionários

#### Listar Todos os Funcionários

```http
GET /funcionarios
```

**Exemplo de Requisição:**

```bash
curl http://localhost:8000/funcionarios
```

**Exemplo de Resposta (200 OK):**

```json
[
  {
    "id": 1,
    "email": "barbeiro@barbearia.com",
    "foto": null,
    "eh_barbeiro": true,
    "eh_admin": false
  },
  {
    "id": 2,
    "email": "admin@barbearia.com",
    "foto": null,
    "eh_barbeiro": false,
    "eh_admin": true
  }
]
```

#### Criar Novo Funcionário

```http
POST /funcionarios
```

**Corpo da Requisição:**

```json
{
  "email": "funcionario@barbearia.com",
  "senha": "SenhaForte123!",
  "foto": null,
  "eh_barbeiro": true,
  "eh_admin": false
}
```

**Exemplo de Resposta (201 Created):**

```json
{
  "id": 3,
  "email": "funcionario@barbearia.com",
  "foto": null,
  "eh_barbeiro": true,
  "eh_admin": false
}
```

---

### Empresa

#### Buscar Dados da Empresa

```http
GET /empresa
```

**Exemplo de Resposta (200 OK):**

```json
{
  "id": 1,
  "nome": "Barbearia Imperial",
  "endereco": "Rua Principal, 123",
  "telefone": "84999887766",
  "email": "contato@barbeariaimperial.com"
}
```

#### Atualizar Dados da Empresa

```http
PUT /empresa
```

**Corpo da Requisição:**

```json
{
  "nome": "Barbearia Imperial Premium",
  "endereco": "Av. Central, 456",
  "telefone": "84988776655",
  "email": "contato@barbeariaimperial.com"
}
```

**Exemplo de Resposta (200 OK):**

```json
{
  "id": 1,
  "nome": "Barbearia Imperial Premium",
  "endereco": "Av. Central, 456",
  "telefone": "84988776655",
  "email": "contato@barbeariaimperial.com"
}
```

> **Nota:** Só existe uma empresa por sistema. Se não existir, será criada. Se já existir, será atualizada.

---

### Horários de Funcionamento

#### Listar Todos os Horários

```http
GET /horarios-funcionamento
```

**Exemplo de Resposta (200 OK):**

```json
[
  {
    "id": 1,
    "dia_semana": 0,
    "hora_inicio": "08:00:00",
    "hora_fim": "18:00:00"
  },
  {
    "id": 2,
    "dia_semana": 1,
    "hora_inicio": "08:00:00",
    "hora_fim": "18:00:00"
  }
]
```

> **Nota:** `dia_semana` segue o padrão: 0 = Segunda, 1 = Terça, ..., 6 = Domingo

#### Criar Horário de Funcionamento

```http
POST /horarios-funcionamento
```

**Corpo da Requisição:**

```json
{
  "dia_semana": 0,
  "hora_inicio": "08:00",
  "hora_fim": "18:00"
}
```

**Exemplo de Resposta (201 Created):**

```json
{
  "id": 1,
  "dia_semana": 0,
  "hora_inicio": "08:00:00",
  "hora_fim": "18:00:00"
}
```

#### Atualizar Horário de Funcionamento

```http
PUT /horarios-funcionamento/{id}
```

**Corpo da Requisição:**

```json
{
  "hora_inicio": "09:00",
  "hora_fim": "19:00"
}
```

**Exemplo de Resposta (200 OK):**

```json
{
  "id": 1,
  "dia_semana": 0,
  "hora_inicio": "09:00:00",
  "hora_fim": "19:00:00"
}
```

#### Deletar Horário de Funcionamento

```http
DELETE /horarios-funcionamento/{id}
```

**Exemplo de Resposta (204 No Content):**

```
(sem corpo de resposta)
```

---

### Agendamentos

#### Listar Todos os Agendamentos

```http
GET /agendamentos
```

**Exemplo de Resposta (200 OK):**

```json
[
  {
    "id": 1,
    "inicio": "2026-02-28T14:00:00",
    "fim": "2026-02-28T15:00:00",
    "cliente_id": 1,
    "barbeiro_id": 2
  },
  {
    "id": 2,
    "inicio": "2026-02-28T15:30:00",
    "fim": "2026-02-28T16:30:00",
    "cliente_id": 3,
    "barbeiro_id": 2
  }
]
```

#### Buscar Agendamento por ID

```http
GET /agendamentos/{agendamento_id}
```

**Exemplo de Resposta (200 OK):**

```json
{
  "id": 1,
  "inicio": "2026-02-28T14:00:00",
  "fim": "2026-02-28T15:00:00",
  "cliente_id": 1,
  "barbeiro_id": 2
}
```

#### Buscar Agendamentos por Cliente

```http
GET /agendamentos/cliente/{cliente_id}
```

**Exemplo de Resposta (200 OK):**

```json
[
  {
    "id": 1,
    "inicio": "2026-02-28T14:00:00",
    "fim": "2026-02-28T15:00:00",
    "cliente_id": 1,
    "barbeiro_id": 2
  }
]
```

#### Buscar Agendamentos por Barbeiro

```http
GET /agendamentos/barbeiro/{barbeiro_id}
```

**Exemplo de Resposta (200 OK):**

```json
[
  {
    "id": 1,
    "inicio": "2026-02-28T14:00:00",
    "fim": "2026-02-28T15:00:00",
    "cliente_id": 1,
    "barbeiro_id": 2
  },
  {
    "id": 2,
    "inicio": "2026-02-28T15:30:00",
    "fim": "2026-02-28T16:30:00",
    "cliente_id": 3,
    "barbeiro_id": 2
  }
]
```

#### Criar Agendamento

```http
POST /agendamentos
```

**Corpo da Requisição:**

```json
{
  "inicio": "2026-03-01T14:00:00",
  "fim": "2026-03-01T15:00:00",
  "cliente_id": 1,
  "barbeiro_id": 2
}
```

**Exemplo de Resposta (201 Created):**

```json
{
  "id": 3,
  "inicio": "2026-03-01T14:00:00",
  "fim": "2026-03-01T15:00:00",
  "cliente_id": 1,
  "barbeiro_id": 2
}
```

> **Validações:**
> - Data/hora de fim deve ser posterior à de início
> - Cliente deve existir no sistema
> - Funcionário deve existir e ser marcado como barbeiro
> - Barbeiro não pode ter outro agendamento no mesmo horário

#### Atualizar Agendamento

```http
PUT /agendamentos/{agendamento_id}
```

**Corpo da Requisição (todos os campos opcionais):**

```json
{
  "inicio": "2026-03-01T15:00:00",
  "fim": "2026-03-01T16:00:00"
}
```

**Exemplo de Resposta (200 OK):**

```json
{
  "id": 3,
  "inicio": "2026-03-01T15:00:00",
  "fim": "2026-03-01T16:00:00",
  "cliente_id": 1,
  "barbeiro_id": 2
}
```

#### Deletar Agendamento

```http
DELETE /agendamentos/{agendamento_id}
```

**Exemplo de Resposta (200 OK):**

```json
{
  "message": "Agendamento deletado com sucesso"
}
```

---

### Estatísticas

#### Obter Estatísticas do Sistema

```http
GET /estatisticas
```

**Exemplo de Resposta (200 OK):**

```json
{
  "clientes": 15,
  "funcionarios": 5,
  "agendamentos": 42
}
```

> **Nota:** Retorna a quantidade total de entidades (linhas) em cada tabela do sistema.

#### Obter Estatísticas de Acesso dos Usuários

```http
GET /estatisticas/acessos
```

**Exemplo de Resposta (200 OK):**

```json
{
  "total_logins": 8,
  "usuarios_que_acessaram": [
    {
      "usuario_id": 1,
      "tipo_usuario": "cliente",
      "email": "cliente@barbearia.com",
      "quantidade_acessos": 5,
      "ultimo_acesso": "2026-03-28T14:30:00"
    },
    {
      "usuario_id": 2,
      "tipo_usuario": "funcionario",
      "email": "funcionario@barbearia.com",
      "quantidade_acessos": 3,
      "ultimo_acesso": "2026-03-28T16:10:00"
    }
  ],
  "ultimo_acesso_por_usuario": [
    {
      "usuario_id": 1,
      "tipo_usuario": "cliente",
      "email": "cliente@barbearia.com",
      "ultimo_acesso": "2026-03-28T14:30:00"
    },
    {
      "usuario_id": 2,
      "tipo_usuario": "funcionario",
      "email": "funcionario@barbearia.com",
      "ultimo_acesso": "2026-03-28T16:10:00"
    }
  ],
  "acessos_por_periodo": {
    "dia": {
      "2026-03-27": 3,
      "2026-03-28": 5
    },
    "semana": {
      "2026-W13": 8
    },
    "mes": {
      "2026-03": 8
    }
  },
  "acessos_por_tipo_usuario": {
    "cliente": 5,
    "funcionario": 3
  }
}
```

> **Nota:** Retorna estatísticas agregadas com base no histórico de logins bem-sucedidos registrados na tabela `acessos_usuario`.

---

#### Obter RelatÃ³rio HTML de Acessos dos UsuÃ¡rios

```http
GET /estatisticas/acessos/relatorio-html
```

**Exemplo de Resposta (200 OK):**

```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <title>Relatorio de Acessos</title>
</head>
<body>
  <header>
    <h1>Relatorio de Acessos dos Usuarios</h1>
  </header>
  <section>
    <h2>Usuarios que acessaram</h2>
  </section>
</body>
</html>
```

> **Nota:** Retorna o relatÃ³rio de acessos em HTML renderizÃ¡vel no navegador, gerado com Template Method a partir das estatÃ­sticas consolidadas de login.

---

## Modelos de Dados

### Cliente

| Campo     | Tipo   | Obrigatório | Descrição                             |
|-----------|--------|-------------|---------------------------------------|
| id        | int    | Não*        | ID único (gerado automaticamente)     |
| email     | string | Sim         | Email do cliente (único no sistema)   |
| senha     | string | Sim**       | Senha com hash bcrypt                 |
| telefone  | string | Sim         | Telefone do cliente                   |
| foto      | string | Não         | URL ou caminho da foto                |

\* Gerado automaticamente ao criar  
\** Obrigatório na criação, nunca retornado nas respostas

**Regras de Validação de Senha:**
- Mínimo 8 caracteres
- Máximo 128 caracteres
- Deve conter pelo menos 3 dos seguintes tipos:
  - Letras maiúsculas
  - Letras minúsculas
  - Números
  - Caracteres especiais (! @ # $ % ^ & * ( ) - _ + = [ ] { } | ')

### Funcionário

| Campo       | Tipo    | Obrigatório | Descrição                             |
|-------------|---------|-------------|---------------------------------------|
| id          | int     | Não*        | ID único (gerado automaticamente)     |
| email       | string  | Sim         | Email do funcionário (único)          |
| senha       | string  | Sim**       | Senha com hash bcrypt                 |
| foto        | string  | Não         | URL ou caminho da foto                |
| eh_barbeiro | boolean | Sim         | Se o funcionário é barbeiro           |
| eh_admin    | boolean | Sim         | Se o funcionário é administrador      |

\* Gerado automaticamente ao criar  
\** Obrigatório na criação, nunca retornado nas respostas

### Empresa

| Campo     | Tipo   | Obrigatório | Descrição                          |
|-----------|--------|-------------|------------------------------------|
| id        | int    | Não*        | ID único (sempre 1)                |
| nome      | string | Não         | Nome da empresa                    |
| endereco  | string | Não         | Endereço da empresa                |
| telefone  | string | Não         | Telefone da empresa                |
| email     | string | Não         | Email de contato da empresa        |

\* Sempre será 1 (apenas uma empresa por sistema)

### Horário de Funcionamento

| Campo        | Tipo | Obrigatório | Descrição                               |
|--------------|------|-------------|-----------------------------------------|
| id           | int  | Não*        | ID único (gerado automaticamente)       |
| dia_semana   | int  | Sim         | Dia da semana (0-6: seg-dom)            |
| hora_inicio  | time | Sim         | Hora de abertura (formato HH:MM)        |
| hora_fim     | time | Sim         | Hora de fechamento (formato HH:MM)      |

\* Gerado automaticamente ao criar

### Agendamento

| Campo       | Tipo     | Obrigatório | Descrição                              |
|-------------|----------|-------------|----------------------------------------|
| id          | int      | Não*        | ID único (gerado automaticamente)      |
| inicio      | datetime | Sim         | Data/hora de início (ISO 8601)         |
| fim         | datetime | Sim         | Data/hora de fim (ISO 8601)            |
| cliente_id  | int      | Sim         | ID do cliente (FK)                     |
| barbeiro_id | int      | Sim         | ID do funcionário barbeiro (FK)        |

\* Gerado automaticamente ao criar

---

## Respostas de Erro

### 400 Bad Request

Retornado quando há erro de validação ou dados inválidos.

```json
{
  "detail": "A senha deve ter no mínimo 8 caracteres"
}
```

### 401 Unauthorized

Retornado quando a autenticação é necessária ou falha.

```json
{
  "detail": "Não autorizado"
}
```

### 404 Not Found

Retornado quando um recurso não é encontrado.

```json
{
  "detail": "Agendamento não encontrado"
}
```

### 409 Conflict

Retornado quando há conflito de dados (ex: email duplicado).

```json
{
  "detail": "Este email já está cadastrado no sistema"
}
```

### 500 Internal Server Error

Retornado quando há erro interno no servidor.

```json
{
  "detail": "Erro interno do servidor. Por favor, tente novamente mais tarde."
}
```
```

**Exemplo de Requisição:**

```bash
curl -X POST http://localhost:8000/funcionarios \
  -H "Content-Type: application/json" \
  -d '{
    "email": "funcionario@barbearia.com",
    "senha": "senha123",
    "eh_barbeiro": true,
    "eh_admin": false
  }'
```

**Exemplo de Resposta (201 Created):**

```json
{
  "id": 3,
  "email": "funcionario@barbearia.com",
  "foto": null,
  "eh_barbeiro": true,
  "eh_admin": false
}
```

---

## Modelos de Dados

### Cliente

| Campo     | Tipo   | Obrigatório | Descrição                    |
|-----------|--------|-------------|------------------------------|
| id        | int    | Não*        | ID único (gerado pelo banco) |
| email     | string | Sim         | Email do cliente             |
| senha     | string | Sim**       | Senha (hash bcrypt)          |
| telefone  | string | Sim         | Telefone do cliente          |
| foto      | string | Não         | URL ou caminho da foto       |

\* Gerado automaticamente ao criar  
\** Obrigatório na criação, nunca retornado nas respostas

### Funcionário

| Campo       | Tipo    | Obrigatório | Descrição                         |
|-------------|---------|-------------|-----------------------------------|
| id          | int     | Não*        | ID único (gerado pelo banco)      |
| email       | string  | Sim         | Email do funcionário              |
| senha       | string  | Sim**       | Senha (hash bcrypt)               |
| foto        | string  | Não         | URL ou caminho da foto            |
| eh_barbeiro | boolean | Sim         | Se o funcionário é barbeiro       |
| eh_admin    | boolean | Sim         | Se o funcionário é administrador  |

\* Gerado automaticamente ao criar  
\** Obrigatório na criação, nunca retornado nas respostas

---

## Respostas de Erro

### 400 Bad Request

Retornado quando há erro de validação ou dados inválidos.

```json
{
  "detail": "Email já cadastrado"
}
```

### 404 Not Found

Retornado quando um recurso não é encontrado.

```json
{
  "detail": "Cliente não encontrado"
}
```

### 500 Internal Server Error

Retornado quando há erro interno no servidor.

```json
{
  "detail": "Erro interno do servidor"
}
```

---

## Testando a API

### Swagger UI (Recomendado)

Acesse a documentação interativa em:

```
http://localhost:8000/docs
```

### ReDoc

Documentação alternativa em:

```
http://localhost:8000/redoc
```

### Exemplos com cURL

```bash
# Login
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "usuario@email.com", "senha": "senha123"}' \
  -c cookies.txt

# Criar agendamento (usando cookie de sessão)
curl -X POST http://localhost:8000/agendamentos \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "inicio": "2026-03-01T14:00:00",
    "fim": "2026-03-01T15:00:00",
    "cliente_id": 1,
    "barbeiro_id": 2
  }'

# Obter estatísticas
curl http://localhost:8000/estatisticas
```

### Exemplos com Python

```python
import requests

# Login
session = requests.Session()
login_data = {
    "email": "usuario@email.com",
    "senha": "senha123"
}
response = session.post('http://localhost:8000/auth/login', json=login_data)
usuario = response.json()
print(f"Logado como: {usuario['email']}")

# Criar agendamento
agendamento_data = {
    "inicio": "2026-03-01T14:00:00",
    "fim": "2026-03-01T15:00:00",
    "cliente_id": 1,
    "barbeiro_id": 2
}
response = session.post('http://localhost:8000/agendamentos', json=agendamento_data)
agendamento = response.json()
print(f"Agendamento criado: {agendamento['id']}")

# Obter estatísticas
response = requests.get('http://localhost:8000/estatisticas')
stats = response.json()
print(f"Estatísticas: {stats}")
```

### Exemplos com JavaScript (fetch)

```javascript
// Login
async function login() {
  const response = await fetch('http://localhost:8000/auth/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    credentials: 'include', // importante para cookies
    body: JSON.stringify({
      email: 'usuario@email.com',
      senha: 'senha123'
    })
  });
  const usuario = await response.json();
  console.log('Logado como:', usuario.email);
}

// Criar agendamento
async function criarAgendamento() {
  const response = await fetch('http://localhost:8000/agendamentos', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    credentials: 'include',
    body: JSON.stringify({
      inicio: '2026-03-01T14:00:00',
      fim: '2026-03-01T15:00:00',
      cliente_id: 1,
      barbeiro_id: 2
    })
  });
  const agendamento = await response.json();
  console.log('Agendamento criado:', agendamento.id);
}

// Obter estatísticas
async function obterEstatisticas() {
  const response = await fetch('http://localhost:8000/estatisticas');
  const stats = await response.json();
  console.log('Estatísticas:', stats);
}
```
