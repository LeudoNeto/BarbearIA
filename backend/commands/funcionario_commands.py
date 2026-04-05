"""
Commands de funcionários.
"""
from commands.base_command import Command


class ListarFuncionariosCommand(Command):
    """Encapsula a listagem de todos os funcionários."""

    def __init__(self, funcionario_manager):
        self._funcionario_manager = funcionario_manager

    def execute(self) -> list:
        return self._funcionario_manager.listar_funcionarios()


class CriarFuncionarioCommand(Command):
    """Encapsula a criação de um novo funcionário."""

    def __init__(self, funcionario_manager, dados: dict):
        self._funcionario_manager = funcionario_manager
        self._dados = dados

    def execute(self) -> dict:
        return self._funcionario_manager.criar_funcionario(self._dados)


class ContarFuncionariosCommand(Command):
    """Encapsula a contagem total de funcionários."""

    def __init__(self, funcionario_manager):
        self._funcionario_manager = funcionario_manager

    def execute(self) -> int:
        return self._funcionario_manager.contar_funcionarios()