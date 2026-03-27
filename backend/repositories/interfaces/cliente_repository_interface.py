from abc import ABC, abstractmethod
from typing import List, Optional
from models.cliente import Cliente

class ClienteRepositoryInterface(ABC):
    @abstractmethod
    def listar(self) -> List[Cliente]:
        """
        Lista todos os clientes.
        
        :return: Lista de objetos Cliente
        """
        pass

    @abstractmethod
    def buscar_por_id(self, cliente_id: int) -> Optional[Cliente]:
        """
        Busca um cliente pelo ID.
        
        :param cliente_id: ID do cliente
        :return: Objeto Cliente ou None se não encontrado
        """
        pass

    @abstractmethod
    def buscar_por_email(self, email: str) -> Optional[Cliente]:
        """
        Busca um cliente pelo email.
        
        :param email: Email do cliente
        :return: Objeto Cliente ou None se não encontrado
        """
        pass

    @abstractmethod
    def criar(self, cliente: Cliente) -> int:
        """
        Cria um novo cliente.
        
        :param cliente: Objeto Cliente
        :return: ID do cliente criado
        """
        pass

    @abstractmethod
    def contar(self) -> int:
        """
        Conta o número total de clientes.
        
        :return: int com a quantidade de clientes
        """
        pass
