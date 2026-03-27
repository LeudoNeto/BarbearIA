from abc import ABC, abstractmethod
from models.empresa import Empresa

class EmpresaRepositoryInterface(ABC):
    @abstractmethod
    def buscar(self) -> Empresa:
        """
        Busca o registro único da empresa.
        
        :return: Objeto Empresa
        :raises NotFoundException: se a empresa não estiver cadastrada
        """
        pass

    @abstractmethod
    def atualizar(self, empresa: Empresa) -> Empresa:
        """
        Atualiza os dados da empresa.
        
        :param empresa: Objeto Empresa com os dados atualizados
        :return: Objeto Empresa atualizado
        """
        pass
