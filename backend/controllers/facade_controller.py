"""
FacadeSingletonController - Facade Pattern para centralizar chamadas aos managers
Este controller atua como uma interface única entre os controllers e os managers,
seguindo o padrão Facade e Singleton.
"""

from managers.auth_manager import auth_manager
from managers.cliente_manager import cliente_manager
from managers.funcionario_manager import funcionario_manager
from managers.empresa_manager import empresa_manager
from managers.horario_funcionamento_manager import horario_funcionamento_manager
from managers.agendamento_manager import agendamento_manager


class FacadeSingletonController:
    """
    Facade Singleton Controller - Interface única para acesso aos managers
    
    Este controller centraliza todas as chamadas aos managers, fornecendo
    uma camada de abstração entre os controllers de rotas e a lógica de negócios.
    """
    
    def __init__(self):
        """Inicializa o facade com referências a todos os managers"""
        self.auth_manager = auth_manager
        self.cliente_manager = cliente_manager
        self.funcionario_manager = funcionario_manager
        self.empresa_manager = empresa_manager
        self.horario_funcionamento_manager = horario_funcionamento_manager
        self.agendamento_manager = agendamento_manager
    
    # ==================== AUTH METHODS ====================
    
    def login(self, dados):
        """
        Realiza login de usuário
        
        :param dados: dict com email e senha
        :return: tuple (dict com dados do usuário, session_id)
        """
        return self.auth_manager.login(dados)
    
    def signup(self, dados):
        """
        Registra um novo cliente
        
        :param dados: dict com dados do cliente
        :return: dict com dados do cliente criado
        """
        return self.auth_manager.signup(dados)
    
    def obter_usuario_logado(self, session_id):
        """
        Obtém dados do usuário logado
        
        :param session_id: ID da sessão
        :return: dict com dados do usuário ou None
        """
        return self.auth_manager.obter_usuario_logado(session_id)
    
    def logout(self, session_id):
        """
        Realiza logout do usuário
        
        :param session_id: ID da sessão
        :return: bool indicando sucesso
        """
        return self.auth_manager.logout(session_id)
    
    # ==================== CLIENTE METHODS ====================
    
    def listar_clientes(self):
        """
        Lista todos os clientes
        
        :return: lista de dicts com dados dos clientes
        """
        return self.cliente_manager.listar_clientes()
    
    def criar_cliente(self, dados):
        """
        Cria um novo cliente
        
        :param dados: dict com dados do cliente
        :return: dict com dados do cliente criado
        """
        return self.cliente_manager.criar_cliente(dados)
    
    # ==================== FUNCIONARIO METHODS ====================
    
    def listar_funcionarios(self):
        """
        Lista todos os funcionários
        
        :return: lista de dicts com dados dos funcionários
        """
        return self.funcionario_manager.listar_funcionarios()
    
    def criar_funcionario(self, dados):
        """
        Cria um novo funcionário
        
        :param dados: dict com dados do funcionário
        :return: dict com dados do funcionário criado
        """
        return self.funcionario_manager.criar_funcionario(dados)
    
    # ==================== EMPRESA METHODS ====================
    
    def buscar_empresa(self):
        """
        Obtém os dados da empresa
        
        :return: dict com dados da empresa ou None
        """
        return self.empresa_manager.buscar_empresa()
    
    def atualizar_empresa(self, dados):
        """
        Atualiza os dados da empresa
        
        :param dados: dict com dados a atualizar
        :return: dict com dados da empresa atualizada
        """
        return self.empresa_manager.atualizar_empresa(dados)
    
    # ==================== HORARIO FUNCIONAMENTO METHODS ====================
    
    def listar_horarios_funcionamento(self):
        """
        Lista todos os horários de funcionamento
        
        :return: lista de dicts com dados dos horários
        """
        return self.horario_funcionamento_manager.listar_horarios()
    
    def criar_horario_funcionamento(self, dados):
        """
        Cria um novo horário de funcionamento
        
        :param dados: dict com dados do horário
        :return: dict com dados do horário criado
        """
        return self.horario_funcionamento_manager.criar_horario(dados)
    
    def atualizar_horario_funcionamento(self, id, dados):
        """
        Atualiza um horário de funcionamento
        
        :param id: ID do horário
        :param dados: dict com dados a atualizar
        :return: dict com dados do horário atualizado
        """
        return self.horario_funcionamento_manager.atualizar_horario(id, dados)
    
    def deletar_horario_funcionamento(self, id):
        """
        Deleta um horário de funcionamento
        
        :param id: ID do horário
        :return: bool indicando sucesso
        """
        return self.horario_funcionamento_manager.deletar_horario(id)
    
    # ==================== AGENDAMENTO METHODS ====================
    
    def listar_agendamentos(self):
        """
        Lista todos os agendamentos
        
        :return: lista de dicts com dados dos agendamentos
        """
        return self.agendamento_manager.listar_agendamentos()
    
    def buscar_agendamento_por_id(self, agendamento_id):
        """
        Busca um agendamento pelo ID
        
        :param agendamento_id: ID do agendamento
        :return: dict com dados do agendamento ou None
        """
        return self.agendamento_manager.buscar_agendamento_por_id(agendamento_id)
    
    def buscar_agendamentos_por_cliente(self, cliente_id):
        """
        Busca todos os agendamentos de um cliente
        
        :param cliente_id: ID do cliente
        :return: lista de dicts com dados dos agendamentos
        """
        return self.agendamento_manager.buscar_agendamentos_por_cliente(cliente_id)
    
    def buscar_agendamentos_por_barbeiro(self, barbeiro_id):
        """
        Busca todos os agendamentos de um barbeiro
        
        :param barbeiro_id: ID do barbeiro
        :return: lista de dicts com dados dos agendamentos
        """
        return self.agendamento_manager.buscar_agendamentos_por_barbeiro(barbeiro_id)
    
    def criar_agendamento(self, dados):
        """
        Cria um novo agendamento
        
        :param dados: dict com dados do agendamento
        :return: dict com dados do agendamento criado
        """
        return self.agendamento_manager.criar_agendamento(dados)
    
    def atualizar_agendamento(self, agendamento_id, dados):
        """
        Atualiza um agendamento existente
        
        :param agendamento_id: ID do agendamento
        :param dados: dict com dados a atualizar
        :return: dict com dados do agendamento atualizado
        """
        return self.agendamento_manager.atualizar_agendamento(agendamento_id, dados)
    
    def deletar_agendamento(self, agendamento_id):
        """
        Deleta um agendamento
        
        :param agendamento_id: ID do agendamento
        :return: bool indicando sucesso
        """
        return self.agendamento_manager.deletar_agendamento(agendamento_id)
    
    # ==================== ESTATÍSTICAS METHODS ====================
    
    def obter_estatisticas_sistema(self):
        """
        Obtém estatísticas gerais do sistema (contagem de todas as entidades)
        
        :return: dict com contagens de todas as entidades
        """
        return {
            'clientes': self.cliente_manager.contar_clientes(),
            'funcionarios': self.funcionario_manager.contar_funcionarios(),
            'agendamentos': self.agendamento_manager.contar_agendamentos()
        }


# Instância singleton
facade_controller = FacadeSingletonController()
