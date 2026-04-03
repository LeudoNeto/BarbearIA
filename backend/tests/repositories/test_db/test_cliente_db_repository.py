import pytest
from exceptions import DuplicateException
from models.cliente import Cliente
from repositories.cliente_db_repository import ClienteDBRepository

@pytest.fixture
def repo():
    return ClienteDBRepository()

@pytest.fixture
def cliente_mock():
    return Cliente(
        email='novo.cliente@barbearia.com',
        senha='senha_criptografada',
        foto='url_foto',
        telefone='83999999999'
    )

def test_criar_e_buscar(repo, cliente_mock):
    novo_id = repo.criar(cliente_mock)
    
    assert novo_id > 0
    cliente_salvo = repo.buscar_por_id(novo_id)
    assert cliente_salvo is not None
    assert cliente_salvo.email == 'novo.cliente@barbearia.com'
    assert cliente_salvo.telefone == '83999999999'

def test_criar_duplicado(repo, cliente_mock):
    repo.criar(cliente_mock)
    with pytest.raises(DuplicateException):
        repo.criar(cliente_mock)

def test_listar_clientes(repo, cliente_mock):
    repo.criar(cliente_mock)
    cliente2 = Cliente(email='segundo@teste.com', senha='abc', telefone='123')
    repo.criar(cliente2)
    
    lista = repo.listar()
    assert len(lista) == 2

def test_contar(repo, cliente_mock):
    repo.criar(cliente_mock)
    assert repo.contar() == 1

def test_buscar_por_email(repo, cliente_mock):
    repo.criar(cliente_mock)
    salvo = repo.buscar_por_email('novo.cliente@barbearia.com')
    assert salvo is not None
    assert salvo.email == 'novo.cliente@barbearia.com'

def test_buscar_nao_encontrado(repo):
    assert repo.buscar_por_id(9999) is None
    assert repo.buscar_por_email('inexistente@123.com') is None
