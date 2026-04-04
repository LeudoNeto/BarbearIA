from datetime import datetime


class Agendamento:
    """Classe que representa um agendamento no sistema"""
    
    def __init__(self, id=None, inicio=None, fim=None, cliente_id=None, barbeiro_id=None, status="Pendente"):
        """
        Inicializa um agendamento
        
        :param id: ID do agendamento
        :param inicio: Data/hora de início (datetime)
        :param fim: Data/hora de fim (datetime)
        :param cliente_id: ID do cliente
        :param barbeiro_id: ID do funcionário (barbeiro)
        :param status: Status atual (Pendente, Confirmado, Cancelado, Concluído)
        """
        self.id = id
        self.inicio = inicio
        self.fim = fim
        self.cliente_id = cliente_id
        self.barbeiro_id = barbeiro_id
        self.status = status
        self._estado = None
        self._inicializar_estado(status)

    def _inicializar_estado(self, status: str):
        """Inicializa a implementação State baseada na string de status"""
        from models.states.estado_pendente import EstadoPendente
        from models.states.estado_confirmado import EstadoConfirmado
        from models.states.estado_cancelado import EstadoCancelado
        from models.states.estado_concluido import EstadoConcluido
        
        estado_map = {
            "Pendente": EstadoPendente,
            "Confirmado": EstadoConfirmado,
            "Cancelado": EstadoCancelado,
            "Concluído": EstadoConcluido
        }
        state_class = estado_map.get(status, EstadoPendente)
        self._estado = state_class(self)

    def confirmar(self):
        """Delega a ação de confirmar ao estado atual"""
        self._estado.confirmar()

    def cancelar(self):
        """Delega a ação de cancelar ao estado atual"""
        self._estado.cancelar()

    def concluir(self):
        """Delega a ação de concluir ao estado atual"""
        self._estado.concluir()
    
    def to_dict(self):
        """Converte o objeto para dicionário"""
        return {
            'id': self.id,
            'inicio': self.inicio.isoformat() if isinstance(self.inicio, datetime) else self.inicio,
            'fim': self.fim.isoformat() if isinstance(self.fim, datetime) else self.fim,
            'cliente_id': self.cliente_id,
            'barbeiro_id': self.barbeiro_id,
            'status': self.status
        }
