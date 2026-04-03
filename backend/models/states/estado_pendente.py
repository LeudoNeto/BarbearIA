from models.states.agendamento_state import AgendamentoState
from exceptions import StateTransitionException


class EstadoPendente(AgendamentoState):
    """Estado inicial, aguardando confirmação."""

    @property
    def nome(self) -> str:
        return "Pendente"

    def confirmar(self):
        from models.states.estado_confirmado import EstadoConfirmado
        self.agendamento._estado = EstadoConfirmado(self.agendamento)
        self.agendamento.status = self.agendamento._estado.nome

    def cancelar(self):
        from models.states.estado_cancelado import EstadoCancelado
        self.agendamento._estado = EstadoCancelado(self.agendamento)
        self.agendamento.status = self.agendamento._estado.nome

    def concluir(self):
        raise StateTransitionException("Um agendamento Pendente não pode ser concluído diretamente. Primeiro ele deve ser confirmado.")
