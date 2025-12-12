from models.cliente import Cliente
from services.senha_service import SenhaService
from repositories.cliente_repository import cliente_repository


class ClienteManager:
    """Manager para orquestrar operações de Cliente"""
    
    def __init__(self):
        """
        Inicializa o manager
        """
        self.cliente_repository = cliente_repository
        self.senha_service = SenhaService()
    
    def listar_clientes(self):
        """
        Lista todos os clientes
        
        :return: lista de dicts com dados dos clientes
        """
        clientes = self.cliente_repository.listar()
        return [cliente.to_dict() for cliente in clientes]
    
    def criar_cliente(self, dados):
        """
        Cria um novo cliente
        
        :param dados: dict com email, senha, telefone e opcionalmente foto
        :return: dict com dados do cliente criado
        """
        email = dados.get('email')
        senha = dados.get('senha')
        telefone = dados.get('telefone')
        foto = dados.get('foto')
                
        # Hash da senha
        senha_hash = self.senha_service.hash_senha(senha)
        
        # Cria o cliente
        cliente = Cliente(
            email=email,
            senha=senha_hash,
            telefone=telefone,
            foto=foto
        )
        
        # Persiste no banco
        cliente_id = self.cliente_repository.criar(cliente)
        cliente.id = cliente_id
        
        return cliente.to_dict()


# Instância singleton
cliente_manager = ClienteManager()
