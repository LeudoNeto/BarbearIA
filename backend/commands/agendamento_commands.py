"""
Commands de agendamentos.
"""
from commands.base_command import Command


class ListarAgendamentosCommand(Command):
    def __init__(self, agendamento_manager):
        self._agendamento_manager = agendamento_manager

    def execute(self) -> list:
        return self._agendamento_manager.listar_agendamentos()


class BuscarAgendamentoPorIdCommand(Command):
    def __init__(self, agendamento_manager, agendamento_id: int):
        self._agendamento_manager = agendamento_manager
        self._id = agendamento_id

    def execute(self) -> dict:
        return self._agendamento_manager.buscar_agendamento_por_id(self._id)


class BuscarAgendamentosPorClienteCommand(Command):
    def __init__(self, agendamento_manager, cliente_id: int):
        self._agendamento_manager = agendamento_manager
        self._cliente_id = cliente_id

    def execute(self) -> list:
        return self._agendamento_manager.buscar_agendamentos_por_cliente(
            self._cliente_id
        )


class BuscarAgendamentosPorBarbeiroCommand(Command):
    def __init__(self, agendamento_manager, barbeiro_id: int):
        self._agendamento_manager = agendamento_manager
        self._barbeiro_id = barbeiro_id

    def execute(self) -> list:
        return self._agendamento_manager.buscar_agendamentos_por_barbeiro(
            self._barbeiro_id
        )


class CriarAgendamentoCommand(Command):
    def __init__(self, agendamento_manager, dados: dict):
        self._agendamento_manager = agendamento_manager
        self._dados = dados

    def execute(self) -> dict:
        return self._agendamento_manager.criar_agendamento(self._dados)


class AtualizarAgendamentoCommand(Command):
    def __init__(self, agendamento_manager, agendamento_id: int, dados: dict):
        self._agendamento_manager = agendamento_manager
        self._id = agendamento_id
        self._dados = dados

    def execute(self) -> dict:
        return self._agendamento_manager.atualizar_agendamento(self._id, self._dados)


class ConfirmarAgendamentoCommand(Command):
    def __init__(self, agendamento_manager, agendamento_id: int):
        self._agendamento_manager = agendamento_manager
        self._id = agendamento_id

    def execute(self) -> dict:
        return self._agendamento_manager.confirmar_agendamento(self._id)


class CancelarAgendamentoCommand(Command):
    def __init__(self, agendamento_manager, agendamento_id: int):
        self._agendamento_manager = agendamento_manager
        self._id = agendamento_id

    def execute(self) -> dict:
        return self._agendamento_manager.cancelar_agendamento(self._id)


class ConcluirAgendamentoCommand(Command):
    def __init__(self, agendamento_manager, agendamento_id: int):
        self._agendamento_manager = agendamento_manager
        self._id = agendamento_id

    def execute(self) -> dict:
        return self._agendamento_manager.concluir_agendamento(self._id)


class DeletarAgendamentoCommand(Command):
    def __init__(self, agendamento_manager, agendamento_id: int):
        self._agendamento_manager = agendamento_manager
        self._id = agendamento_id

    def execute(self) -> bool:
        return self._agendamento_manager.deletar_agendamento(self._id)


class ContarAgendamentosCommand(Command):
    def __init__(self, agendamento_manager):
        self._agendamento_manager = agendamento_manager

    def execute(self) -> int:
        return self._agendamento_manager.contar_agendamentos()