from abc import ABC, abstractmethod


class AgendamentoState(ABC):
    """Interface abstrata para os estados de um agendamento."""

    def __init__(self, agendamento):
        self.agendamento = agendamento

    @property
    @abstractmethod
    def nome(self) -> str:
        """Retorna o nome do estado (ex: 'Pendente')"""
        pass

    @abstractmethod
    def confirmar(self):
        """Tenta fazer a transição para Confirmado"""
        pass

    @abstractmethod
    def cancelar(self):
        """Tenta fazer a transição para Cancelado"""
        pass

    @abstractmethod
    def concluir(self):
        """Tenta fazer a transição para Concluído"""
        pass
