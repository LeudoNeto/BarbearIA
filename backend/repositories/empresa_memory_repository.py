from models.empresa import Empresa
from repositories.interfaces.empresa_repository_interface import EmpresaRepositoryInterface


class EmpresaMemoryRepository(EmpresaRepositoryInterface):
    """Repositório em memória para operações de persistência de Empresa"""

    def __init__(self):
        """
        Inicializa o repositório com um registro padrão da empresa
        """
        self._empresa = Empresa(
            id=1,
            nome='Minha Barbearia',
            descricao='Barbearia moderna com os melhores profissionais.',
            endereco='Rua Exemplo, 123 - Centro',
            cnpj='00.000.000/0001-00',
            telefone='(00) 00000-0000',
            email='contato@minhabarbearia.com'
        )

    def buscar(self):
        """
        Busca o registro único da empresa

        :return: Objeto Empresa
        """
        return self._empresa

    def atualizar(self, empresa):
        """
        Atualiza os dados da empresa

        :param empresa: Objeto Empresa com os dados atualizados
        :return: Objeto Empresa atualizado
        """
        self._empresa = empresa
        return self._empresa


# Instância singleton
empresa_memory_repository = EmpresaMemoryRepository()
