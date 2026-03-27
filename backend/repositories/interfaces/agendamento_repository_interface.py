from abc import ABC, abstractmethod
from typing import List, Optional
from models.agendamento import Agendamento

class AgendamentoRepositoryInterface(ABC):
    @abstractmethod
    def listar(self) -> List[Agendamento]:
        """
        Lista todos os agendamentos.
        
        :return: Lista de objetos Agendamento
        """
        ...

    @abstractmethod
    def buscar_por_id(self, agendamento_id: int) -> Optional[Agendamento]:
        """
        Busca um agendamento pelo ID.
        
        :param agendamento_id: ID do agendamento
        :return: Objeto Agendamento ou None se não encontrado
        """
        ...

    @abstractmethod
    def buscar_por_cliente(self, cliente_id: int) -> List[Agendamento]:
        """
        Busca todos os agendamentos de um cliente.
        
        :param cliente_id: ID do cliente
        :return: Lista de objetos Agendamento
        """
        ...

    @abstractmethod
    def buscar_por_barbeiro(self, barbeiro_id: int) -> List[Agendamento]:
        """
        Busca todos os agendamentos de um barbeiro.
        
        :param barbeiro_id: ID do barbeiro
        :return: Lista de objetos Agendamento
        """
        ...

    @abstractmethod
    def criar(self, agendamento: Agendamento) -> int:
        """
        Cria um novo agendamento.
        
        :param agendamento: Objeto Agendamento
        :return: ID do agendamento criado
        """
        ...

    @abstractmethod
    def atualizar(self, agendamento: Agendamento) -> bool:
        """
        Atualiza um agendamento existente.
        
        :param agendamento: Objeto Agendamento com dados atualizados
        :return: bool indicando sucesso
        """
        ...

    @abstractmethod
    def deletar(self, agendamento_id: int) -> bool:
        """
        Deleta um agendamento.
        
        :param agendamento_id: ID do agendamento
        :return: bool indicando sucesso
        """
        ...

    @abstractmethod
    def contar(self) -> int:
        """
        Conta o número total de agendamentos.
        
        :return: int com a quantidade de agendamentos
        """
        ...
