from fastapi.testclient import TestClient
import pytest


@pytest.fixture(scope='session', autouse=True)
def setup_test_database():
    """Sobrescreve setup global para manter este teste sem dependencia de MySQL."""
    yield


@pytest.fixture(autouse=True)
def limpa_tabelas():
    """Sobrescreve limpeza global para manter este teste isolado do banco."""
    yield


class FacadeStub:
    def __init__(self):
        self.calls = []

    def _record(self, method_name, *args, **kwargs):
        self.calls.append((method_name, args, kwargs))

    def last(self, method_name):
        for call in reversed(self.calls):
            if call[0] == method_name:
                return call
        raise AssertionError(f'Nenhuma chamada registrada para {method_name}')

    # Auth
    def login(self, dados):
        self._record('login', dados)
        return {'id': 1, 'email': dados['email'], 'tipo': 'cliente'}, 'sess-123'

    def obter_usuario_logado(self, session_id):
        self._record('obter_usuario_logado', session_id)
        return {'id': 1, 'email': 'user@email.com', 'tipo': 'cliente'}

    def logout(self, session_id):
        self._record('logout', session_id)

    def signup(self, dados):
        self._record('signup', dados)
        return {'id': 2, 'email': dados['email'], 'telefone': dados['telefone']}

    # Cliente
    def listar_clientes(self):
        self._record('listar_clientes')
        return [{'id': 1, 'email': 'cliente@email.com'}]

    def criar_cliente(self, dados):
        self._record('criar_cliente', dados)
        return {'id': 3, **dados}

    # Funcionario
    def listar_funcionarios(self):
        self._record('listar_funcionarios')
        return [{'id': 1, 'email': 'funcionario@email.com'}]

    def criar_funcionario(self, dados):
        self._record('criar_funcionario', dados)
        return {'id': 4, **dados}

    # Empresa
    def buscar_empresa(self):
        self._record('buscar_empresa')
        return {'id': 1, 'nome': 'BarbearIA'}

    def atualizar_empresa(self, dados):
        self._record('atualizar_empresa', dados)
        return {'id': 1, **dados}

    def desfazer_ultima_atualizacao_empresa(self):
        self._record('desfazer_ultima_atualizacao_empresa')
        return {'id': 1, 'nome': 'BarbearIA restaurada'}

    # Horarios
    def listar_horarios_funcionamento(self):
        self._record('listar_horarios_funcionamento')
        return [{'id': 1, 'dia_semana': 1}]

    def criar_horario_funcionamento(self, dados):
        self._record('criar_horario_funcionamento', dados)
        return {'id': 1, **dados}

    def atualizar_horario_funcionamento(self, horario_id, dados):
        self._record('atualizar_horario_funcionamento', horario_id, dados)
        return {'id': horario_id, **dados}

    def deletar_horario_funcionamento(self, horario_id):
        self._record('deletar_horario_funcionamento', horario_id)

    # Agendamentos
    def listar_agendamentos(self):
        self._record('listar_agendamentos')
        return [{'id': 10}]

    def buscar_agendamento_por_id(self, agendamento_id):
        self._record('buscar_agendamento_por_id', agendamento_id)
        return {'id': agendamento_id}

    def buscar_agendamentos_por_cliente(self, cliente_id):
        self._record('buscar_agendamentos_por_cliente', cliente_id)
        return [{'id': 11, 'cliente_id': cliente_id}]

    def buscar_agendamentos_por_barbeiro(self, barbeiro_id):
        self._record('buscar_agendamentos_por_barbeiro', barbeiro_id)
        return [{'id': 12, 'barbeiro_id': barbeiro_id}]

    def criar_agendamento(self, dados):
        self._record('criar_agendamento', dados)
        return {'id': 13, **dados}

    def atualizar_agendamento(self, agendamento_id, dados):
        self._record('atualizar_agendamento', agendamento_id, dados)
        return {'id': agendamento_id, **dados}

    def confirmar_agendamento(self, agendamento_id):
        self._record('confirmar_agendamento', agendamento_id)
        return {'id': agendamento_id, 'estado': 'confirmado'}

    def cancelar_agendamento(self, agendamento_id):
        self._record('cancelar_agendamento', agendamento_id)
        return {'id': agendamento_id, 'estado': 'cancelado'}

    def concluir_agendamento(self, agendamento_id):
        self._record('concluir_agendamento', agendamento_id)
        return {'id': agendamento_id, 'estado': 'concluido'}

    def deletar_agendamento(self, agendamento_id):
        self._record('deletar_agendamento', agendamento_id)

    # Estatisticas
    def obter_estatisticas_sistema(self):
        self._record('obter_estatisticas_sistema')
        return {'clientes': 1, 'funcionarios': 1, 'agendamentos': 1}

    def obter_estatisticas_acesso(self):
        self._record('obter_estatisticas_acesso')
        return {'total_logins': 10}

    def gerar_relatorio_acessos_html(self):
        self._record('gerar_relatorio_acessos_html')
        return '<html><body>Relatorio</body></html>'

    def gerar_relatorio_acessos_pdf(self):
        self._record('gerar_relatorio_acessos_pdf')
        return b'%PDF-1.4 fake'

    # Preview
    def gerar_preview_corte(self, imagem_pessoa_bytes, imagem_corte_bytes, usar_mock=False):
        self._record('gerar_preview_corte', imagem_pessoa_bytes, imagem_corte_bytes, usar_mock)
        return {'ok': True, 'usar_mock': usar_mock}


@pytest.fixture
def facade_stub(monkeypatch):
    from controllers.auth_controller import auth_controller
    from controllers.cliente_controller import cliente_controller
    from controllers.funcionario_controller import funcionario_controller
    from controllers.empresa_controller import empresa_controller
    from controllers.horario_funcionamento_controller import horario_funcionamento_controller
    from controllers.agendamento_controller import agendamento_controller
    from controllers.estatisticas_controller import estatisticas_controller
    from controllers.preview_corte_controller import preview_corte_controller

    stub = FacadeStub()
    controllers = [
        auth_controller,
        cliente_controller,
        funcionario_controller,
        empresa_controller,
        horario_funcionamento_controller,
        agendamento_controller,
        estatisticas_controller,
        preview_corte_controller,
    ]

    for controller in controllers:
        monkeypatch.setattr(controller, 'facade', stub)

    return stub


@pytest.fixture
def client(facade_stub):
    from main import app

    return TestClient(app)


def assert_last_call(facade_stub, method_name, *expected_args):
    name, args, _ = facade_stub.last(method_name)
    assert name == method_name
    assert args == expected_args


def test_root(client):
    response = client.get('/')

    assert response.status_code == 200
    assert response.json()['message'] == 'BarbearIA API'


def test_auth_login(client, facade_stub):
    payload = {'email': 'user@email.com', 'senha': '123'}

    response = client.post('/auth/login', json=payload)

    assert response.status_code == 200
    assert response.json()['email'] == payload['email']
    assert response.cookies.get('session_id') == 'sess-123'
    assert_last_call(facade_stub, 'login', payload)


def test_auth_me(client, facade_stub):
    response = client.get('/auth/me', cookies={'session_id': 'sess-123'})

    assert response.status_code == 200
    assert response.json()['id'] == 1
    assert_last_call(facade_stub, 'obter_usuario_logado', 'sess-123')


def test_auth_logout(client, facade_stub):
    response = client.post('/auth/logout', cookies={'session_id': 'sess-123'})

    assert response.status_code == 200
    assert response.json()['message'] == 'Logout realizado com sucesso'
    assert 'session_id=' in response.headers['set-cookie']
    assert_last_call(facade_stub, 'logout', 'sess-123')


def test_auth_signup(client, facade_stub):
    payload = {'email': 'novo@email.com', 'senha': '123', 'telefone': '99999999'}

    response = client.post('/auth/signup', json=payload)

    assert response.status_code == 201
    assert response.json()['email'] == payload['email']
    assert_last_call(facade_stub, 'signup', payload)


def test_listar_clientes(client, facade_stub):
    response = client.get('/clientes')

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert_last_call(facade_stub, 'listar_clientes')


def test_criar_cliente(client, facade_stub):
    payload = {'email': 'cliente@email.com', 'senha': '123', 'telefone': '9999'}

    response = client.post('/clientes', json=payload)

    assert response.status_code == 201
    assert response.json()['email'] == payload['email']
    assert_last_call(facade_stub, 'criar_cliente', payload)


def test_listar_funcionarios(client, facade_stub):
    response = client.get('/funcionarios')

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert_last_call(facade_stub, 'listar_funcionarios')


def test_criar_funcionario(client, facade_stub):
    payload = {'email': 'func@email.com', 'senha': '123', 'eh_barbeiro': True, 'eh_admin': False}

    response = client.post('/funcionarios', json=payload)

    assert response.status_code == 201
    assert response.json()['email'] == payload['email']
    assert_last_call(facade_stub, 'criar_funcionario', payload)


def test_buscar_empresa(client, facade_stub):
    response = client.get('/empresa')

    assert response.status_code == 200
    assert response.json()['nome'] == 'BarbearIA'
    assert_last_call(facade_stub, 'buscar_empresa')


def test_atualizar_empresa(client, facade_stub):
    payload = {'nome': 'BarbearIA Premium'}

    response = client.put('/empresa', json=payload)

    assert response.status_code == 200
    assert response.json()['nome'] == payload['nome']
    assert_last_call(facade_stub, 'atualizar_empresa', payload)


def test_desfazer_ultima_atualizacao_empresa(client, facade_stub):
    response = client.post('/empresa/desfazer-ultima-atualizacao')

    assert response.status_code == 200
    assert response.json()['nome'] == 'BarbearIA restaurada'
    assert_last_call(facade_stub, 'desfazer_ultima_atualizacao_empresa')


def test_listar_horarios_funcionamento(client, facade_stub):
    response = client.get('/horarios-funcionamento')

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert_last_call(facade_stub, 'listar_horarios_funcionamento')


def test_criar_horario_funcionamento(client, facade_stub):
    payload = {'dia_semana': 1, 'hora_abertura': '08:00', 'hora_fechamento': '18:00'}

    response = client.post('/horarios-funcionamento', json=payload)

    assert response.status_code == 201
    assert response.json()['dia_semana'] == 1
    assert_last_call(facade_stub, 'criar_horario_funcionamento', payload)


def test_atualizar_horario_funcionamento(client, facade_stub):
    payload = {'hora_abertura': '09:00'}

    response = client.put('/horarios-funcionamento/1', json=payload)

    assert response.status_code == 200
    assert response.json()['id'] == 1
    assert_last_call(facade_stub, 'atualizar_horario_funcionamento', 1, payload)


def test_deletar_horario_funcionamento(client, facade_stub):
    response = client.delete('/horarios-funcionamento/1')

    assert response.status_code == 204
    assert response.text == ''
    assert_last_call(facade_stub, 'deletar_horario_funcionamento', 1)


def test_listar_agendamentos(client, facade_stub):
    response = client.get('/agendamentos')

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert_last_call(facade_stub, 'listar_agendamentos')


def test_buscar_agendamento_por_id(client, facade_stub):
    response = client.get('/agendamentos/10')

    assert response.status_code == 200
    assert response.json()['id'] == 10
    assert_last_call(facade_stub, 'buscar_agendamento_por_id', 10)


def test_buscar_agendamentos_por_cliente(client, facade_stub):
    response = client.get('/agendamentos/cliente/20')

    assert response.status_code == 200
    assert response.json()[0]['cliente_id'] == 20
    assert_last_call(facade_stub, 'buscar_agendamentos_por_cliente', 20)


def test_buscar_agendamentos_por_barbeiro(client, facade_stub):
    response = client.get('/agendamentos/barbeiro/30')

    assert response.status_code == 200
    assert response.json()[0]['barbeiro_id'] == 30
    assert_last_call(facade_stub, 'buscar_agendamentos_por_barbeiro', 30)


def test_criar_agendamento(client, facade_stub):
    payload = {
        'inicio': '2026-01-01T10:00:00',
        'fim': '2026-01-01T11:00:00',
        'cliente_id': 1,
        'barbeiro_id': 2,
    }

    response = client.post('/agendamentos', json=payload)

    assert response.status_code == 201
    assert response.json()['cliente_id'] == 1
    assert_last_call(facade_stub, 'criar_agendamento', payload)


def test_atualizar_agendamento(client, facade_stub):
    payload = {'fim': '2026-01-01T11:30:00'}

    response = client.put('/agendamentos/10', json=payload)

    assert response.status_code == 200
    assert response.json()['id'] == 10
    assert_last_call(facade_stub, 'atualizar_agendamento', 10, payload)


def test_confirmar_agendamento(client, facade_stub):
    response = client.patch('/agendamentos/10/confirmar')

    assert response.status_code == 200
    assert response.json()['estado'] == 'confirmado'
    assert_last_call(facade_stub, 'confirmar_agendamento', 10)


def test_cancelar_agendamento(client, facade_stub):
    response = client.patch('/agendamentos/10/cancelar')

    assert response.status_code == 200
    assert response.json()['estado'] == 'cancelado'
    assert_last_call(facade_stub, 'cancelar_agendamento', 10)


def test_concluir_agendamento(client, facade_stub):
    response = client.patch('/agendamentos/10/concluir')

    assert response.status_code == 200
    assert response.json()['estado'] == 'concluido'
    assert_last_call(facade_stub, 'concluir_agendamento', 10)


def test_deletar_agendamento(client, facade_stub):
    response = client.delete('/agendamentos/10')

    assert response.status_code == 200
    assert response.json()['message'] == 'Agendamento deletado com sucesso'
    assert_last_call(facade_stub, 'deletar_agendamento', 10)


def test_obter_estatisticas_sistema(client, facade_stub):
    response = client.get('/estatisticas')

    assert response.status_code == 200
    assert response.json()['clientes'] == 1
    assert_last_call(facade_stub, 'obter_estatisticas_sistema')


def test_obter_estatisticas_acesso(client, facade_stub):
    response = client.get('/estatisticas/acessos')

    assert response.status_code == 200
    assert response.json()['total_logins'] == 10
    assert_last_call(facade_stub, 'obter_estatisticas_acesso')


def test_obter_relatorio_html_acessos(client, facade_stub):
    response = client.get('/estatisticas/acessos/relatorio-html')

    assert response.status_code == 200
    assert '<html>' in response.text
    assert response.headers['content-type'].startswith('text/html')
    assert_last_call(facade_stub, 'gerar_relatorio_acessos_html')


def test_obter_relatorio_pdf_acessos(client, facade_stub):
    response = client.get('/estatisticas/acessos/relatorio-pdf')

    assert response.status_code == 200
    assert response.content == b'%PDF-1.4 fake'
    assert response.headers['content-type'].startswith('application/pdf')
    assert 'relatorio_acessos.pdf' in response.headers['content-disposition']
    assert_last_call(facade_stub, 'gerar_relatorio_acessos_pdf')


def test_gerar_preview_corte(client, facade_stub):
    files = {
        'imagem_pessoa': ('pessoa.jpg', b'pessoa-bytes', 'image/jpeg'),
        'imagem_corte': ('corte.jpg', b'corte-bytes', 'image/jpeg'),
    }
    data = {'usar_mock': 'true'}

    response = client.post('/preview-corte', files=files, data=data)

    assert response.status_code == 200
    assert response.json()['ok'] is True
    assert response.json()['usar_mock'] is True
    assert_last_call(
        facade_stub,
        'gerar_preview_corte',
        b'pessoa-bytes',
        b'corte-bytes',
        True,
    )