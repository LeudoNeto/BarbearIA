from models.states.agendamento_state import AgendamentoState
from exceptions import StateTransitionException


class EstadoConcluido(AgendamentoState):
    """Estado indicando que o agendamento foi concluído."""

    @property
    def nome(self) -> str:
        return "Concluído"

    def confirmar(self):
        raise StateTransitionException("O agendamento já foi concluído e não pode voltar a ser confirmado.")

    def cancelar(self):
        raise StateTransitionException("Um agendamento já concluído não pode ser cancelado.")

    def concluir(self):
        raise StateTransitionException("O agendamento já está concluído.")
