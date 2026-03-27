import pytest
from exceptions import DatabaseException, DuplicateException, NotFoundException
from models.funcionario import Funcionario
from repositories.funcionario_db_repository import FuncionarioDBRepository

@pytest.fixture
def repo():
    return FuncionarioDBRepository()

@pytest.fixture
def funcionario_mock():
    return Funcionario(
        email='admin@barbearia.com',
        senha='senha_criptografada',
        foto='url_foto',
        eh_barbeiro=False,
        eh_admin=True
    )

def test_criar_e_buscar(repo, funcionario_mock):
    novo_id = repo.criar(funcionario_mock)
    assert novo_id > 0
    
    salvo = repo.buscar_por_id(novo_id)
    assert salvo.email == 'admin@barbearia.com'
    assert salvo.eh_admin is True

def test_criar_duplicado(repo, funcionario_mock):
    repo.criar(funcionario_mock)
    with pytest.raises(DuplicateException):
        repo.criar(funcionario_mock)

def test_listar(repo, funcionario_mock):
    repo.criar(funcionario_mock)
    func2 = Funcionario(
        email='b2@barbearia.com',
        senha='abc',
        eh_barbeiro=True,
        eh_admin=False
    )
    repo.criar(func2)
    
    lista = repo.listar()
    assert len(lista) == 2

def test_buscar_por_email(repo, funcionario_mock):
    repo.criar(funcionario_mock)
    salvo = repo.buscar_por_email('admin@barbearia.com')
    assert salvo is not None
    assert salvo.eh_admin is True

def test_contar(repo, funcionario_mock):
    repo.criar(funcionario_mock)
    assert repo.contar() == 1
