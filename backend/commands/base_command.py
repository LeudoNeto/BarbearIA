"""
Command Pattern - Interface base para todos os comandos do sistema.
"""
from abc import ABC, abstractmethod
from typing import Any


class Command(ABC):
    """
    Interface abstrata para todos os comandos da aplicação.
    Cada comando encapsula uma operação de negócio completa,
    incluindo seus dados e a chamada ao manager responsável.
    """

    @abstractmethod
    def execute(self) -> Any:
        """
        Executa a operação encapsulada pelo comando.

        :return: resultado da operação (varia por comando)
        """