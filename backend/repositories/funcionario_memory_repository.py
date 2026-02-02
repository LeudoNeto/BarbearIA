from exceptions import DuplicateException


class FuncionarioMemoryRepository:
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


# Instância singleton
funcionario_memory_repository = FuncionarioMemoryRepository()
