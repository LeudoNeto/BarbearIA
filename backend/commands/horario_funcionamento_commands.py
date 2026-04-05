"""
Commands de horários de funcionamento.
"""
from commands.base_command import Command


class ListarHorariosCommand(Command):
    def __init__(self, horario_manager):
        self._horario_manager = horario_manager

    def execute(self) -> list:
        return self._horario_manager.listar_horarios()


class CriarHorarioCommand(Command):
    def __init__(self, horario_manager, dados: dict):
        self._horario_manager = horario_manager
        self._dados = dados

    def execute(self) -> dict:
        return self._horario_manager.criar_horario(self._dados)


class AtualizarHorarioCommand(Command):
    def __init__(self, horario_manager, horario_id: int, dados: dict):
        self._horario_manager = horario_manager
        self._id = horario_id
        self._dados = dados

    def execute(self) -> dict:
        return self._horario_manager.atualizar_horario(self._id, self._dados)


class DeletarHorarioCommand(Command):
    def __init__(self, horario_manager, horario_id: int):
        self._horario_manager = horario_manager
        self._id = horario_id

    def execute(self) -> None:
        return self._horario_manager.deletar_horario(self._id)