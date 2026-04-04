"""
Commands de clientes.
"""
from commands.base_command import Command


class ListarClientesCommand(Command):
    """Encapsula a listagem de todos os clientes."""

    def __init__(self, cliente_manager):
        self._cliente_manager = cliente_manager

    def execute(self) -> list:
        return self._cliente_manager.listar_clientes()


class CriarClienteCommand(Command):
    """Encapsula a criação de um novo cliente."""

    def __init__(self, cliente_manager, dados: dict):
        self._cliente_manager = cliente_manager
        self._dados = dados

    def execute(self) -> dict:
        return self._cliente_manager.criar_cliente(self._dados)


class ContarClientesCommand(Command):
    """Encapsula a contagem total de clientes."""

    def __init__(self, cliente_manager):
        self._cliente_manager = cliente_manager

    def execute(self) -> int:
        return self._cliente_manager.contar_clientes()