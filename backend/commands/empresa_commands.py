"""
Commands de empresa.
"""
from commands.base_command import Command


class BuscarEmpresaCommand(Command):
    """Encapsula a busca dos dados da empresa."""

    def __init__(self, empresa_manager):
        self._empresa_manager = empresa_manager

    def execute(self) -> dict:
        return self._empresa_manager.buscar_empresa()


class AtualizarEmpresaCommand(Command):
    """Encapsula a atualização dos dados da empresa."""

    def __init__(self, empresa_manager, dados: dict):
        self._empresa_manager = empresa_manager
        self._dados = dados

    def execute(self) -> dict:
        return self._empresa_manager.atualizar_empresa(self._dados)


class DesfazerAtualizacaoEmpresaCommand(Command):
    """Encapsula o undo da última atualização da empresa (Memento)."""

    def __init__(self, empresa_manager):
        self._empresa_manager = empresa_manager

    def execute(self) -> dict:
        return self._empresa_manager.desfazer_ultima_atualizacao()