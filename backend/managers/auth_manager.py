from datetime import datetime

from exceptions import ValidationException
from managers.cliente_manager import cliente_manager
from models.acesso_usuario import AcessoUsuario
from repositories.repository_factory import repository_factory
from services.senha_service import SenhaService
from services.session_service import session_service


class AuthManager:
    """Manager para orquestrar operacoes de autenticacao."""

    def __init__(self):
        """
        Inicializa o manager.
        """
        self.cliente_repository = repository_factory.get_cliente_repository()
        self.funcionario_repository = repository_factory.get_funcionario_repository()
        self.acesso_usuario_repository = repository_factory.get_acesso_usuario_repository()
        self.senha_service = SenhaService()
        self.session_service = session_service

    def login(self, dados: dict):
        """
        Realiza login de usuario (cliente ou funcionario) e cria uma sessao.

        :param dados: dict contendo email e senha
        :return: tuple (dict com dados do usuario e tipo, session_id)
        :raises ValidationException: se credenciais invalidas
        """
        email = dados.get('email')
        senha = dados.get('senha')

        if not email or not email.strip():
            raise ValidationException("Email e obrigatorio")

        if not senha or not senha.strip():
            raise ValidationException("Senha e obrigatoria")

        cliente = self.cliente_repository.buscar_por_email(email)
        if cliente:
            if self.senha_service.verificar_senha(senha, cliente.senha):
                usuario_dict = cliente.to_dict()
                usuario_dict['tipo'] = 'cliente'
                usuario_dict['telefone'] = cliente.telefone
                session_id = self.session_service.criar_sessao(usuario_dict)
                self._registrar_acesso(cliente.id, 'cliente', cliente.email)
                return usuario_dict, session_id
            raise ValidationException("Email ou senha invalidos")

        funcionario = self.funcionario_repository.buscar_por_email(email)
        if funcionario:
            if self.senha_service.verificar_senha(senha, funcionario.senha):
                usuario_dict = funcionario.to_dict()
                usuario_dict['tipo'] = 'funcionario'
                usuario_dict['eh_barbeiro'] = funcionario.eh_barbeiro
                usuario_dict['eh_admin'] = funcionario.eh_admin
                session_id = self.session_service.criar_sessao(usuario_dict)
                self._registrar_acesso(funcionario.id, 'funcionario', funcionario.email)
                return usuario_dict, session_id
            raise ValidationException("Email ou senha invalidos")

        raise ValidationException("Email ou senha invalidos")

    def signup(self, dados: dict):
        """
        Registra um novo cliente no sistema.

        :param dados: dict com email, senha, telefone e opcionalmente foto
        :return: dict com dados do cliente criado
        """
        return cliente_manager.criar_cliente(dados)

    def obter_usuario_logado(self, session_id: str):
        """
        Obtem os dados do usuario logado a partir da sessao.

        :param session_id: ID da sessao
        :return: dict com dados do usuario ou None se sessao invalida
        """
        usuario = self.session_service.obter_usuario_da_sessao(session_id)
        if usuario:
            self.session_service.renovar_sessao(session_id)
        return usuario

    def logout(self, session_id: str):
        """
        Realiza logout do usuario destruindo a sessao.

        :param session_id: ID da sessao
        :return: bool indicando se logout foi bem sucedido
        """
        return self.session_service.destruir_sessao(session_id)

    def _registrar_acesso(self, usuario_id: int, tipo_usuario: str, email: str):
        """Registra um login bem-sucedido no historico de acessos."""
        acesso_usuario = AcessoUsuario(
            usuario_id=usuario_id,
            tipo_usuario=tipo_usuario,
            email=email,
            data_hora_acesso=datetime.now()
        )
        self.acesso_usuario_repository.criar(acesso_usuario)


auth_manager = AuthManager()
