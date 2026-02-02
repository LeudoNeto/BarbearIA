from models.cliente import Cliente
from services.senha_service import SenhaService
from services.validacao_service import ValidacaoService
from repositories.repository_factory import repository_factory


class ClienteManager:
    """Manager para orquestrar operações de Cliente"""
    
    def __init__(self):
        """
        Inicializa o manager
        """
        self.cliente_repository = repository_factory.get_cliente_repository()
        self.senha_service = SenhaService()
        self.validacao_service = ValidacaoService()
    
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
        
        # Valida email e senha
        self.validacao_service.validar_email(email)
        self.validacao_service.validar_senha(senha, email=email)
                
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
