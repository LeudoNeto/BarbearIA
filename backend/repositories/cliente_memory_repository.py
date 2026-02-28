from exceptions import DuplicateException


class ClienteMemoryRepository:
    """Repositório em memória para operações de persistência de Cliente"""
    
    def __init__(self):
        """
        Inicializa o repositório em memória
        """
        self._clientes = {}  # Dicionário id -> Cliente
        self._next_id = 1
    
    def listar(self):
        """
        Lista todos os clientes
        
        :return: Lista de objetos Cliente
        """
        return list(self._clientes.values())
    
    def buscar_por_id(self, cliente_id):
        """
        Busca um cliente pelo ID
        
        :param cliente_id: ID do cliente
        :return: Objeto Cliente ou None se não encontrado
        """
        return self._clientes.get(cliente_id)
    
    def buscar_por_email(self, email):
        """
        Busca um cliente pelo email
        
        :param email: Email do cliente
        :return: Objeto Cliente ou None se não encontrado
        """
        for cliente in self._clientes.values():
            if cliente.email == email:
                return cliente
        return None
    
    def criar(self, cliente):
        """
        Cria um novo cliente em memória
        
        :param cliente: Objeto Cliente
        :return: ID do cliente criado
        """
        # Verifica se email já existe
        for existing_cliente in self._clientes.values():
            if existing_cliente.email == cliente.email:
                raise DuplicateException("Este email já está cadastrado no sistema")
        
        # Atribui ID e armazena
        cliente.id = self._next_id
        self._clientes[self._next_id] = cliente
        self._next_id += 1
        
        return cliente.id
    
    def contar(self):
        """
        Conta o número total de clientes
        
        :return: int com a quantidade de clientes
        """
        return len(self._clientes)


# Instância singleton
cliente_memory_repository = ClienteMemoryRepository()
