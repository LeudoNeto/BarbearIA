from models.agendamento import Agendamento
from exceptions import NotFoundException


class AgendamentoMemoryRepository:
    """Repositório em memória para operações de persistência de Agendamento"""
    
    def __init__(self):
        """
        Inicializa o repositório em memória
        """
        self._agendamentos = {}  # Dicionário id -> Agendamento
        self._next_id = 1
    
    def listar(self):
        """
        Lista todos os agendamentos
        
        :return: Lista de objetos Agendamento
        """
        return list(self._agendamentos.values())
    
    def buscar_por_id(self, agendamento_id):
        """
        Busca um agendamento pelo ID
        
        :param agendamento_id: ID do agendamento
        :return: Objeto Agendamento ou None se não encontrado
        """
        return self._agendamentos.get(agendamento_id)
    
    def buscar_por_cliente(self, cliente_id):
        """
        Busca todos os agendamentos de um cliente
        
        :param cliente_id: ID do cliente
        :return: Lista de objetos Agendamento
        """
        return [a for a in self._agendamentos.values() if a.cliente_id == cliente_id]
    
    def buscar_por_barbeiro(self, barbeiro_id):
        """
        Busca todos os agendamentos de um barbeiro
        
        :param barbeiro_id: ID do barbeiro
        :return: Lista de objetos Agendamento
        """
        return [a for a in self._agendamentos.values() if a.barbeiro_id == barbeiro_id]
    
    def criar(self, agendamento):
        """
        Cria um novo agendamento em memória
        
        :param agendamento: Objeto Agendamento
        :return: ID do agendamento criado
        """
        # Atribui ID e armazena
        agendamento.id = self._next_id
        self._agendamentos[self._next_id] = agendamento
        self._next_id += 1
        
        return agendamento.id
    
    def atualizar(self, agendamento):
        """
        Atualiza um agendamento existente
        
        :param agendamento: Objeto Agendamento com dados atualizados
        :return: bool indicando sucesso
        """
        if agendamento.id not in self._agendamentos:
            raise NotFoundException("Agendamento não encontrado")
        
        self._agendamentos[agendamento.id] = agendamento
        return True
    
    def deletar(self, agendamento_id):
        """
        Deleta um agendamento
        
        :param agendamento_id: ID do agendamento
        :return: bool indicando sucesso
        """
        if agendamento_id not in self._agendamentos:
            raise NotFoundException("Agendamento não encontrado")
        
        del self._agendamentos[agendamento_id]
        return True
    
    def contar(self):
        """
        Conta o número total de agendamentos
        
        :return: int com a quantidade de agendamentos
        """
        return len(self._agendamentos)


# Instância singleton
agendamento_memory_repository = AgendamentoMemoryRepository()
