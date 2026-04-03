from abc import ABC, abstractmethod
from typing import List, Optional
from models.funcionario import Funcionario

class FuncionarioRepositoryInterface(ABC):
    @abstractmethod
    def listar(self) -> List[Funcionario]:
        """
        Lista todos os funcionários.
        
        :return: Lista de objetos Funcionario
        """
        pass

    @abstractmethod
    def buscar_por_id(self, funcionario_id: int) -> Optional[Funcionario]:
        """
        Busca um funcionário pelo ID.
        
        :param funcionario_id: ID do funcionário
        :return: Objeto Funcionario ou None se não encontrado
        """
        pass

    @abstractmethod
    def buscar_por_email(self, email: str) -> Optional[Funcionario]:
        """
        Busca um funcionário pelo email.
        
        :param email: Email do funcionário
        :return: Objeto Funcionario ou None se não encontrado
        """
        pass

    @abstractmethod
    def criar(self, funcionario: Funcionario) -> int:
        """
        Cria um novo funcionário.
        
        :param funcionario: Objeto Funcionario
        :return: ID do funcionário criado
        """
        pass

    @abstractmethod
    def contar(self) -> int:
        """
        Conta o número total de funcionários.
        
        :return: int com a quantidade de funcionários
        """
        pass
