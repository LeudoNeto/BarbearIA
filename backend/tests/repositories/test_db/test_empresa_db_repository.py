import pytest
from exceptions import NotFoundException
from models.empresa import Empresa
from repositories.empresa_db_repository import EmpresaDBRepository

@pytest.fixture
def repo():
    return EmpresaDBRepository()

@pytest.fixture
def empresa_mock():
    return Empresa(
        id=1,
        nome='Barbearia Central',
        descricao='Melhor corte da cidade',
        endereco='Rua Principal, 123',
        cnpj='00.000.000/0001-00',
        telefone='83999999999',
        email='contato@barbeariacentral.com'
    )

def test_buscar_existente(repo):
    """Garante que a empresa primária (seed) pode ser buscada e alterada nativamente"""
    res = repo.buscar()
    assert res is not None
    assert type(res.nome) is str # A seed foi inserida pelo conftest.py

def test_atualizar(repo, empresa_mock):
    res_buscado = repo.buscar()
    
    empresa_mock.id = res_buscado.id
    res = repo.atualizar(empresa_mock)
    
    assert res.nome == 'Barbearia Central'
    assert repo.buscar().nome == 'Barbearia Central'

def test_atualizar_not_found(repo, empresa_mock):
    empresa_mock.id = 9999
    with pytest.raises(NotFoundException):
         repo.atualizar(empresa_mock)
