from exceptions import DuplicateException
from repositories.interfaces.funcionario_repository_interface import FuncionarioRepositoryInterface


class FuncionarioMemoryRepository(FuncionarioRepositoryInterface):
    """Repositório em memória para operações de persistência de Funcionario"""
    
    def __init__(self):
        """
        Inicializa o repositório em memória
        """
        self._funcionarios = {}  # Dicionário id -> Funcionario
        self._next_id = 1
    
    def listar(self):
        """
        Lista todos os funcionários
        
        :return: Lista de objetos Funcionario
        """
        return list(self._funcionarios.values())
    
    def buscar_por_id(self, funcionario_id):
        """
        Busca um funcionário pelo ID
        
        :param funcionario_id: ID do funcionário
        :return: Objeto Funcionario ou None se não encontrado
        """
        return self._funcionarios.get(funcionario_id)
    
    def buscar_por_email(self, email):
        """
        Busca um funcionário pelo email
        
        :param email: Email do funcionário
        :return: Objeto Funcionario ou None se não encontrado
        """
        for funcionario in self._funcionarios.values():
            if funcionario.email == email:
                return funcionario
        return None
    
    def criar(self, funcionario):
        """
        Cria um novo funcionário em memória
        
        :param funcionario: Objeto Funcionario
        :return: ID do funcionário criado
        """
        # Verifica se email já existe
        for existing_funcionario in self._funcionarios.values():
            if existing_funcionario.email == funcionario.email:
                raise DuplicateException("Este email já está cadastrado no sistema")
        
        # Atribui ID e armazena
        funcionario.id = self._next_id
        self._funcionarios[self._next_id] = funcionario
        self._next_id += 1
        
        return funcionario.id
    
    def contar(self):
        """
        Conta o número total de funcionários
        
        :return: int com a quantidade de funcionários
        """
        return len(self._funcionarios)


# Instância singleton
funcionario_memory_repository = FuncionarioMemoryRepository()
