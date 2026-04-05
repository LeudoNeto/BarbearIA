from models.states.agendamento_state import AgendamentoState
from exceptions import StateTransitionException


class EstadoConfirmado(AgendamentoState):
    """Estado indicando que o agendamento foi confirmado."""

    @property
    def nome(self) -> str:
        return "Confirmado"

    def confirmar(self):
        raise StateTransitionException("O agendamento já está confirmado.")

    def cancelar(self):
        from models.states.estado_cancelado import EstadoCancelado
        self.agendamento._estado = EstadoCancelado(self.agendamento)
        self.agendamento.status = self.agendamento._estado.nome

    def concluir(self):
        from models.states.estado_concluido import EstadoConcluido
        self.agendamento._estado = EstadoConcluido(self.agendamento)
        self.agendamento.status = self.agendamento._estado.nome
