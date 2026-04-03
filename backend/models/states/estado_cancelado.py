from models.states.agendamento_state import AgendamentoState
from exceptions import StateTransitionException


class EstadoCancelado(AgendamentoState):
    """Estado indicando que o agendamento foi cancelado."""

    @property
    def nome(self) -> str:
        return "Cancelado"

    def confirmar(self):
        raise StateTransitionException("Um agendamento cancelado não pode ser confirmado.")

    def cancelar(self):
        raise StateTransitionException("O agendamento já está cancelado.")

    def concluir(self):
        raise StateTransitionException("Um agendamento cancelado não pode ser concluído.")
