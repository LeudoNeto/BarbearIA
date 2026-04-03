"""
FacadeSingletonController - Facade Pattern para centralizar chamadas aos managers.
Este controller atua como uma interface unica entre os controllers e os managers,
seguindo o padrao Facade e Singleton.
"""

from managers.agendamento_manager import agendamento_manager
from managers.auth_manager import auth_manager
from managers.cliente_manager import cliente_manager
from managers.empresa_manager import empresa_manager
from managers.estatisticas_acesso_manager import estatisticas_acesso_manager
from managers.funcionario_manager import funcionario_manager
from managers.horario_funcionamento_manager import horario_funcionamento_manager
from managers.preview_corte_manager import preview_corte_manager
from managers.relatorio_acesso_manager import relatorio_acesso_manager


class FacadeSingletonController:
    """
    Facade Singleton Controller - Interface unica para acesso aos managers.

    Este controller centraliza todas as chamadas aos managers, fornecendo
    uma camada de abstracao entre os controllers de rotas e a logica de negocios.
    """

    _instance = None
    _initialized = False

    def __new__(cls):
        """Implementacao do padrao Singleton para garantir instancia unica."""
        if cls._instance is None:
            cls._instance = super(FacadeSingletonController, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        """Inicializa o facade com referencias a todos os managers apenas uma vez."""
        if FacadeSingletonController._initialized:
            return

        self.auth_manager = auth_manager
        self.cliente_manager = cliente_manager
        self.funcionario_manager = funcionario_manager
        self.empresa_manager = empresa_manager
        self.horario_funcionamento_manager = horario_funcionamento_manager
        self.agendamento_manager = agendamento_manager
        self.estatisticas_acesso_manager = estatisticas_acesso_manager
        self.preview_corte_manager = preview_corte_manager
        self.relatorio_acesso_manager = relatorio_acesso_manager

        FacadeSingletonController._initialized = True

    # ==================== AUTH METHODS ====================

    def login(self, dados):
        """
        Realiza login de usuario.

        :param dados: dict com email e senha
        :return: tuple (dict com dados do usuario, session_id)
        """
        return self.auth_manager.login(dados)

    def signup(self, dados):
        """
        Registra um novo cliente.

        :param dados: dict com dados do cliente
        :return: dict com dados do cliente criado
        """
        return self.auth_manager.signup(dados)

    def obter_usuario_logado(self, session_id):
        """
        Obtem dados do usuario logado.

        :param session_id: ID da sessao
        :return: dict com dados do usuario ou None
        """
        return self.auth_manager.obter_usuario_logado(session_id)

    def logout(self, session_id):
        """
        Realiza logout do usuario.

        :param session_id: ID da sessao
        :return: bool indicando sucesso
        """
        return self.auth_manager.logout(session_id)

    # ==================== CLIENTE METHODS ====================

    def listar_clientes(self):
        """
        Lista todos os clientes.

        :return: lista de dicts com dados dos clientes
        """
        return self.cliente_manager.listar_clientes()

    def criar_cliente(self, dados):
        """
        Cria um novo cliente.

        :param dados: dict com dados do cliente
        :return: dict com dados do cliente criado
        """
        return self.cliente_manager.criar_cliente(dados)

    # ==================== FUNCIONARIO METHODS ====================

    def listar_funcionarios(self):
        """
        Lista todos os funcionarios.

        :return: lista de dicts com dados dos funcionarios
        """
        return self.funcionario_manager.listar_funcionarios()

    def criar_funcionario(self, dados):
        """
        Cria um novo funcionario.

        :param dados: dict com dados do funcionario
        :return: dict com dados do funcionario criado
        """
        return self.funcionario_manager.criar_funcionario(dados)

    # ==================== EMPRESA METHODS ====================

    def buscar_empresa(self):
        """
        Obtem os dados da empresa.

        :return: dict com dados da empresa ou None
        """
        return self.empresa_manager.buscar_empresa()

    def atualizar_empresa(self, dados):
        """
        Atualiza os dados da empresa.

        :param dados: dict com dados a atualizar
        :return: dict com dados da empresa atualizada
        """
        return self.empresa_manager.atualizar_empresa(dados)

    def desfazer_ultima_atualizacao_empresa(self):
        """
        Desfaz a última atualização dos dados da empresa.

        :return: dict com os dados restaurados da empresa
        """
        return self.empresa_manager.desfazer_ultima_atualizacao()

    # ==================== HORARIO FUNCIONAMENTO METHODS ====================

    def listar_horarios_funcionamento(self):
        """
        Lista todos os horarios de funcionamento.

        :return: lista de dicts com dados dos horarios
        """
        return self.horario_funcionamento_manager.listar_horarios()

    def criar_horario_funcionamento(self, dados):
        """
        Cria um novo horario de funcionamento.

        :param dados: dict com dados do horario
        :return: dict com dados do horario criado
        """
        return self.horario_funcionamento_manager.criar_horario(dados)

    def atualizar_horario_funcionamento(self, id, dados):
        """
        Atualiza um horario de funcionamento.

        :param id: ID do horario
        :param dados: dict com dados a atualizar
        :return: dict com dados do horario atualizado
        """
        return self.horario_funcionamento_manager.atualizar_horario(id, dados)

    def deletar_horario_funcionamento(self, id):
        """
        Deleta um horario de funcionamento.

        :param id: ID do horario
        :return: bool indicando sucesso
        """
        return self.horario_funcionamento_manager.deletar_horario(id)

    # ==================== AGENDAMENTO METHODS ====================

    def listar_agendamentos(self):
        """
        Lista todos os agendamentos.

        :return: lista de dicts com dados dos agendamentos
        """
        return self.agendamento_manager.listar_agendamentos()

    def buscar_agendamento_por_id(self, agendamento_id):
        """
        Busca um agendamento pelo ID.

        :param agendamento_id: ID do agendamento
        :return: dict com dados do agendamento ou None
        """
        return self.agendamento_manager.buscar_agendamento_por_id(agendamento_id)

    def buscar_agendamentos_por_cliente(self, cliente_id):
        """
        Busca todos os agendamentos de um cliente.

        :param cliente_id: ID do cliente
        :return: lista de dicts com dados dos agendamentos
        """
        return self.agendamento_manager.buscar_agendamentos_por_cliente(cliente_id)

    def buscar_agendamentos_por_barbeiro(self, barbeiro_id):
        """
        Busca todos os agendamentos de um barbeiro.

        :param barbeiro_id: ID do barbeiro
        :return: lista de dicts com dados dos agendamentos
        """
        return self.agendamento_manager.buscar_agendamentos_por_barbeiro(barbeiro_id)

    def criar_agendamento(self, dados):
        """
        Cria um novo agendamento.

        :param dados: dict com dados do agendamento
        :return: dict com dados do agendamento criado
        """
        return self.agendamento_manager.criar_agendamento(dados)

    def atualizar_agendamento(self, agendamento_id, dados):
        """
        Atualiza um agendamento existente.

        :param agendamento_id: ID do agendamento
        :param dados: dict com dados a atualizar
        :return: dict com dados do agendamento atualizado
        """
        return self.agendamento_manager.atualizar_agendamento(agendamento_id, dados)

    def deletar_agendamento(self, agendamento_id):
        """
        Deleta um agendamento.

        :param agendamento_id: ID do agendamento
        :return: bool indicando sucesso
        """
        return self.agendamento_manager.deletar_agendamento(agendamento_id)

    # ==================== ESTATISTICAS METHODS ====================

    def obter_estatisticas_sistema(self):
        """
        Obtem estatisticas gerais do sistema (contagem de todas as entidades).

        :return: dict com contagens de todas as entidades
        """
        return {
            'clientes': self.cliente_manager.contar_clientes(),
            'funcionarios': self.funcionario_manager.contar_funcionarios(),
            'agendamentos': self.agendamento_manager.contar_agendamentos()
        }

    def obter_estatisticas_acesso(self):
        """
        Obtem estatisticas agregadas de acesso dos usuarios.

        :return: dict com dados consolidados dos acessos
        """
        return self.estatisticas_acesso_manager.obter_estatisticas_acesso()

    def gerar_relatorio_acessos_html(self):
        """
        Gera o relatorio de acessos em HTML.

        :return: string HTML com o relatorio consolidado
        """
        return self.relatorio_acesso_manager.gerar_relatorio_acessos_html()

    def gerar_relatorio_acessos_pdf(self):
        """
        Gera o relatorio de acessos em PDF.

        :return: bytes do PDF com o relatorio consolidado
        """
        return self.relatorio_acesso_manager.gerar_relatorio_acessos_pdf()

    # ==================== PREVIEW CORTE METHODS ====================

    def gerar_preview_corte(self, imagem_pessoa_bytes: bytes, imagem_corte_bytes: bytes, usar_mock: bool = False):
        """
        Gera preview de corte com IA.

        :param imagem_pessoa_bytes: bytes da imagem da pessoa
        :param imagem_corte_bytes: bytes da imagem de referencia do corte
        :param usar_mock: forca strategy mockada para testes
        :return: dict com caminho do preview e strategy utilizada
        """
        return self.preview_corte_manager.gerar_preview_corte(
            imagem_pessoa_bytes=imagem_pessoa_bytes,
            imagem_corte_bytes=imagem_corte_bytes,
            usar_mock=usar_mock
        )


facade_controller = FacadeSingletonController()
