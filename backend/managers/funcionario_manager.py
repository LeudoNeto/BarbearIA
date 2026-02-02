from models.funcionario import Funcionario
from services.senha_service import SenhaService
from services.validacao_service import ValidacaoService
from repositories.funcionario_repository import funcionario_repository


class FuncionarioManager:
    """Manager para orquestrar operações de Funcionario"""
    
    def __init__(self):
        """
        Inicializa o manager
        """
        self.funcionario_repository = funcionario_repository
        self.senha_service = SenhaService()
        self.validacao_service = ValidacaoService()
    
    def listar_funcionarios(self):
        """
        Lista todos os funcionários
        
        :return: lista de dicts com dados dos funcionários
        """
        funcionarios = self.funcionario_repository.listar()
        return [funcionario.to_dict() for funcionario in funcionarios]
    
    def criar_funcionario(self, dados):
        """
        Cria um novo funcionário
        
        :param dados: dict com email, senha, eh_barbeiro, eh_admin e opcionalmente foto
        :return: dict com dados do funcionário criado
        """
        email = dados.get('email')
        senha = dados.get('senha')
        eh_barbeiro = dados.get('eh_barbeiro', False)
        eh_admin = dados.get('eh_admin', False)
        foto = dados.get('foto')
        
        # Valida email e senha
        self.validacao_service.validar_email(email)
        self.validacao_service.validar_senha(senha, email=email)
                
        # Hash da senha
        senha_hash = self.senha_service.hash_senha(senha)
        
        # Cria o funcionário
        funcionario = Funcionario(
            email=email,
            senha=senha_hash,
            foto=foto,
            eh_barbeiro=bool(eh_barbeiro),
            eh_admin=bool(eh_admin)
        )
        
        # Persiste no banco
        funcionario_id = self.funcionario_repository.criar(funcionario)
        funcionario.id = funcionario_id
        
        return funcionario.to_dict()


# Instância singleton
funcionario_manager = FuncionarioManager()
