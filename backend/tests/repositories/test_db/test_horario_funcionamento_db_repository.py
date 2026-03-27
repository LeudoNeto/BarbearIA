import pytest
from exceptions import NotFoundException, DuplicateException
from models.horario_funcionamento import HorarioFuncionamento
from repositories.horario_funcionamento_db_repository import HorarioFuncionamentoDBRepository

@pytest.fixture
def repo():
    return HorarioFuncionamentoDBRepository()

@pytest.fixture
def horario_mock():
    return HorarioFuncionamento(
        dia_semana=1,
        hora_inicio="08:00",
        hora_fim="18:00"
    )

def test_criar_e_buscar(repo, horario_mock):
    novo_id = repo.criar(horario_mock)
    assert novo_id > 0
    
    salvo = repo.buscar_por_id(novo_id)
    assert salvo.dia_semana == 1
    assert salvo.hora_fim == "18:00:00"

def test_criar_duplicado(repo, horario_mock):
    repo.criar(horario_mock)
    with pytest.raises(DuplicateException):
        repo.criar(horario_mock)

def test_listar_por_dia(repo, horario_mock):
    repo.criar(horario_mock)
    
    horario2 = HorarioFuncionamento(
        dia_semana=2,
        hora_inicio="09:00",
        hora_fim="12:00"
    )
    repo.criar(horario2)
    
    res = repo.listar_por_dia(1)
    assert len(res) == 1
    assert res[0].dia_semana == 1
    
    res_todos = repo.listar()
    assert len(res_todos) == 2

def test_atualizar(repo, horario_mock):
    id_novo = repo.criar(horario_mock)
    horario_salvo = repo.buscar_por_id(id_novo)
    
    horario_salvo.hora_fim = "20:00"
    repo.atualizar(horario_salvo)
    
    atualizado = repo.buscar_por_id(id_novo)
    assert atualizado.hora_fim == "20:00:00"

def test_deletar(repo, horario_mock):
    id_novo = repo.criar(horario_mock)
    repo.deletar(id_novo)
    with pytest.raises(NotFoundException):
        repo.buscar_por_id(id_novo)
