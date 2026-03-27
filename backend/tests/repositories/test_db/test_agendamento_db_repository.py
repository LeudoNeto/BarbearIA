import pytest
from datetime import datetime
from exceptions import DatabaseException, NotFoundException
from models.agendamento import Agendamento
from models.cliente import Cliente
from models.funcionario import Funcionario
from repositories.agendamento_db_repository import AgendamentoDBRepository
from repositories.cliente_db_repository import ClienteDBRepository
from repositories.funcionario_db_repository import FuncionarioDBRepository

@pytest.fixture
def repo():
    return AgendamentoDBRepository()

@pytest.fixture
def dependencias():
    # Precisamos criar Cliente e Funcionario reais porque o Agendamento os utiliza como FK!
    cliente_repo = ClienteDBRepository()
    c_id = cliente_repo.criar(Cliente(email='c@x.com', senha='abc', telefone='123'))
    
    func_repo = FuncionarioDBRepository()
    f_id = func_repo.criar(Funcionario(email='f@x.com', senha='abc', eh_barbeiro=True))
    
    return {'cliente_id': c_id, 'barbeiro_id': f_id}

def test_criar_e_buscar(repo, dependencias):
    agend = Agendamento(
        inicio=datetime(2025, 2, 2, 8, 0),
        fim=datetime(2025, 2, 2, 9, 0),
        cliente_id=dependencias['cliente_id'],
        barbeiro_id=dependencias['barbeiro_id']
    )
    
    novo_id = repo.criar(agend)
    assert novo_id > 0
    
    res = repo.buscar_por_id(novo_id)
    assert res is not None
    assert res.cliente_id == dependencias['cliente_id']
    assert res.barbeiro_id == dependencias['barbeiro_id']
    assert res.inicio == datetime(2025, 2, 2, 8, 0)

def test_listar(repo, dependencias):
    agend = Agendamento(
        inicio=datetime(2025, 2, 2, 8, 0),
        fim=datetime(2025, 2, 2, 9, 0),
        cliente_id=dependencias['cliente_id'],
        barbeiro_id=dependencias['barbeiro_id']
    )
    repo.criar(agend)
    
    lista = repo.listar()
    assert len(lista) == 1
    
    busca_cli = repo.buscar_por_cliente(dependencias['cliente_id'])
    assert len(busca_cli) == 1

def test_fk_erro(repo):
    # Forçando FK Error, deve emitir a exception de BD nossa.
    agend = Agendamento(
        inicio=datetime(2025, 2, 2, 8, 0),
        fim=datetime(2025, 2, 2, 9, 0),
        cliente_id=99999, # Nao existe
        barbeiro_id=99999
    )
    with pytest.raises(DatabaseException):
         repo.criar(agend)

def test_deletar(repo, dependencias):
    agend = Agendamento(
        inicio=datetime(2025, 2, 2, 8, 0),
        fim=datetime(2025, 2, 2, 9, 0),
        cliente_id=dependencias['cliente_id'],
        barbeiro_id=dependencias['barbeiro_id']
    )
    novo_id = repo.criar(agend)
    
    assert repo.deletar(novo_id) is True
    assert repo.buscar_por_id(novo_id) is None

def test_deletar_nao_encontrado(repo):
    with pytest.raises(NotFoundException):
        repo.deletar(999999)
