import pytest

from exceptions import ValidationException
from managers import empresa_manager as empresa_manager_module
from models.empresa import Empresa


@pytest.fixture(scope='session', autouse=True)
def setup_test_database():
    """Sobrescreve setup global de banco para manter este teste unitario."""
    yield


@pytest.fixture(autouse=True)
def limpa_tabelas():
    """Sobrescreve limpeza global de tabelas para evitar dependencia de MySQL."""
    yield


class FakeEmpresaRepository:
    def __init__(self):
        self._empresa = Empresa(
            id=1,
            nome='Minha Barbearia',
            descricao='Barbearia moderna com os melhores profissionais.',
            endereco='Rua Exemplo, 123 - Centro',
            cnpj='00.000.000/0001-00',
            telefone='(00) 00000-0000',
            email='contato@minhabarbearia.com'
        )

    def buscar(self):
        return Empresa(**self._empresa.to_dict())

    def atualizar(self, empresa):
        self._empresa = Empresa(**empresa.to_dict())
        return self._empresa


@pytest.fixture
def manager(monkeypatch):
    fake_repository = FakeEmpresaRepository()
    monkeypatch.setattr(
        empresa_manager_module.repository_factory,
        'get_empresa_repository',
        lambda: fake_repository
    )
    return empresa_manager_module.EmpresaManager()


def test_desfazer_ultima_atualizacao_empresa(manager):
    estado_original = manager.buscar_empresa()

    resultado_atualizacao = manager.atualizar_empresa({'nome': 'Barbearia Premium'})
    assert resultado_atualizacao['nome'] == 'Barbearia Premium'

    estado_restaurado = manager.desfazer_ultima_atualizacao()

    assert estado_restaurado['nome'] == estado_original['nome']
    assert estado_restaurado == estado_original


def test_desfazer_sem_historico_disponivel_lanca_erro(manager):
    with pytest.raises(ValidationException, match='Não há atualização de empresa para desfazer'):
        manager.desfazer_ultima_atualizacao()


def test_desfazer_apenas_uma_vez_por_snapshot(manager):
    manager.atualizar_empresa({'descricao': 'Nova descrição'})
    manager.desfazer_ultima_atualizacao()

    with pytest.raises(ValidationException):
        manager.desfazer_ultima_atualizacao()
