import pytest
from datetime import datetime
from models.agendamento import Agendamento
from exceptions import StateTransitionException


def test_agendamento_inicia_pendente():
    agendamento = Agendamento(id=1, inicio=datetime.now(), fim=datetime.now(), cliente_id=1, barbeiro_id=2)
    assert agendamento.status == "Pendente"
    assert agendamento._estado is not None
    assert agendamento._estado.nome == "Pendente"

def test_agendamento_confirmar_sucesso():
    agendamento = Agendamento(id=1, inicio=datetime.now(), fim=datetime.now(), cliente_id=1, barbeiro_id=2)
    agendamento.confirmar()
    assert agendamento.status == "Confirmado"
    assert agendamento._estado.nome == "Confirmado"

def test_agendamento_cancelar_do_pendente():
    agendamento = Agendamento(id=1, inicio=datetime.now(), fim=datetime.now(), cliente_id=1, barbeiro_id=2)
    agendamento.cancelar()
    assert agendamento.status == "Cancelado"

def test_agendamento_cancelar_do_confirmado():
    agendamento = Agendamento(id=1, inicio=datetime.now(), fim=datetime.now(), cliente_id=1, barbeiro_id=2, status="Confirmado")
    agendamento.cancelar()
    assert agendamento.status == "Cancelado"

def test_agendamento_concluir_do_confirmado():
    agendamento = Agendamento(id=1, inicio=datetime.now(), fim=datetime.now(), cliente_id=1, barbeiro_id=2, status="Confirmado")
    agendamento.concluir()
    assert agendamento.status == "Concluído"

def test_agendamento_concluir_pendente_falha():
    agendamento = Agendamento(id=1, inicio=datetime.now(), fim=datetime.now(), cliente_id=1, barbeiro_id=2)
    with pytest.raises(StateTransitionException):
        agendamento.concluir()

def test_agendamento_interagir_cancelado_falha():
    agendamento = Agendamento(id=1, inicio=datetime.now(), fim=datetime.now(), cliente_id=1, barbeiro_id=2, status="Cancelado")
    with pytest.raises(StateTransitionException):
        agendamento.confirmar()
    with pytest.raises(StateTransitionException):
        agendamento.concluir()
    with pytest.raises(StateTransitionException):
        agendamento.cancelar()

def test_agendamento_interagir_concluido_falha():
    agendamento = Agendamento(id=1, inicio=datetime.now(), fim=datetime.now(), cliente_id=1, barbeiro_id=2, status="Concluído")
    with pytest.raises(StateTransitionException):
        agendamento.confirmar()
    with pytest.raises(StateTransitionException):
        agendamento.cancelar()
    with pytest.raises(StateTransitionException):
        agendamento.concluir()
