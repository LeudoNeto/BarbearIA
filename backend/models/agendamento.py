from datetime import datetime


class Agendamento:
    """Classe que representa um agendamento no sistema"""
    
    def __init__(self, id=None, inicio=None, fim=None, cliente_id=None, barbeiro_id=None):
        """
        Inicializa um agendamento
        
        :param id: ID do agendamento
        :param inicio: Data/hora de início (datetime)
        :param fim: Data/hora de fim (datetime)
        :param cliente_id: ID do cliente
        :param barbeiro_id: ID do funcionário (barbeiro)
        """
        self.id = id
        self.inicio = inicio
        self.fim = fim
        self.cliente_id = cliente_id
        self.barbeiro_id = barbeiro_id
    
    def to_dict(self):
        """Converte o objeto para dicionário"""
        return {
            'id': self.id,
            'inicio': self.inicio.isoformat() if isinstance(self.inicio, datetime) else self.inicio,
            'fim': self.fim.isoformat() if isinstance(self.fim, datetime) else self.fim,
            'cliente_id': self.cliente_id,
            'barbeiro_id': self.barbeiro_id
        }
