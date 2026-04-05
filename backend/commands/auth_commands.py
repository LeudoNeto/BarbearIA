"""
Commands de autenticação.
"""
from typing import Any, Tuple

from commands.base_command import Command


class LoginCommand(Command):
    """Encapsula a operação de login de um usuário."""

    def __init__(self, auth_manager, dados: dict):
        self._auth_manager = auth_manager
        self._dados = dados

    def execute(self) -> Tuple[dict, str]:
        return self._auth_manager.login(self._dados)


class SignupCommand(Command):
    """Encapsula o registro de um novo cliente via autenticação."""

    def __init__(self, auth_manager, dados: dict):
        self._auth_manager = auth_manager
        self._dados = dados

    def execute(self) -> dict:
        return self._auth_manager.signup(self._dados)


class ObterUsuarioLogadoCommand(Command):
    """Encapsula a consulta do usuário autenticado na sessão."""

    def __init__(self, auth_manager, session_id: str):
        self._auth_manager = auth_manager
        self._session_id = session_id

    def execute(self) -> dict:
        return self._auth_manager.obter_usuario_logado(self._session_id)


class LogoutCommand(Command):
    """Encapsula a operação de logout."""

    def __init__(self, auth_manager, session_id: str):
        self._auth_manager = auth_manager
        self._session_id = session_id

    def execute(self) -> bool:
        return self._auth_manager.logout(self._session_id)