from services.senha_service import SenhaService
from services.session_service import session_service
from repositories.repository_factory import repository_factory
from managers.cliente_manager import cliente_manager
from exceptions import ValidationException


class AuthManager:
    """Manager para orquestrar operações de autenticação"""

    def __init__(self):
        """
        Inicializa o manager
        """
        self.cliente_repository = repository_factory.get_cliente_repository()
        self.funcionario_repository = repository_factory.get_funcionario_repository()
        self.senha_service = SenhaService()
        self.session_service = session_service

    def login(self, dados: dict):
        """
        Realiza login de usuário (cliente ou funcionário) e cria uma sessão

        :param dados: dict contendo email e senha
        :return: tuple (dict com dados do usuário e tipo, session_id)
        :raises ValidationException: se credenciais inválidas
        """
        # Extração dos dados
        email = dados.get('email')
        senha = dados.get('senha')
        
        # Validações básicas
        if not email or not email.strip():
            raise ValidationException("Email é obrigatório")
        
        if not senha or not senha.strip():
            raise ValidationException("Senha é obrigatória")

        # Busca primeiro como cliente
        cliente = self.cliente_repository.buscar_por_email(email)
        if cliente:
            if self.senha_service.verificar_senha(senha, cliente.senha):
                usuario_dict = cliente.to_dict()
                usuario_dict['tipo'] = 'cliente'
                usuario_dict['telefone'] = cliente.telefone
                session_id = self.session_service.criar_sessao(usuario_dict)
                return usuario_dict, session_id
            else:
                raise ValidationException("Email ou senha inválidos")

        # Se não achou como cliente, busca como funcionário
        funcionario = self.funcionario_repository.buscar_por_email(email)
        if funcionario:
            if self.senha_service.verificar_senha(senha, funcionario.senha):
                usuario_dict = funcionario.to_dict()
                usuario_dict['tipo'] = 'funcionario'
                usuario_dict['eh_barbeiro'] = funcionario.eh_barbeiro
                usuario_dict['eh_admin'] = funcionario.eh_admin
                session_id = self.session_service.criar_sessao(usuario_dict)
                return usuario_dict, session_id
            else:
                raise ValidationException("Email ou senha inválidos")

        # Usuário não encontrado
        raise ValidationException("Email ou senha inválidos")

    def signup(self, dados: dict):
        """
        Registra um novo cliente no sistema

        :param dados: dict com email, senha, telefone e opcionalmente foto
        :return: dict com dados do cliente criado
        """
        return cliente_manager.criar_cliente(dados)
    
    def obter_usuario_logado(self, session_id: str):
        """
        Obtém os dados do usuário logado a partir da sessão

        :param session_id: ID da sessão
        :return: dict com dados do usuário ou None se sessão inválida
        """
        usuario = self.session_service.obter_usuario_da_sessao(session_id)
        if usuario:
            # Renova a sessão a cada acesso
            self.session_service.renovar_sessao(session_id)
        return usuario
    
    def logout(self, session_id: str):
        """
        Realiza logout do usuário destruindo a sessão

        :param session_id: ID da sessão
        :return: bool indicando se logout foi bem sucedido
        """
        return self.session_service.destruir_sessao(session_id)


# Instância singleton
auth_manager = AuthManager()
