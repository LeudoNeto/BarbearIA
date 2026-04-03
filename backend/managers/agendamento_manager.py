from models.agendamento import Agendamento
from repositories.repository_factory import repository_factory
from services.validacao_agendamento_service import ValidacaoAgendamentoService
from exceptions import NotFoundException
from services.observer import Observable
from services.observers.agendamento_logging_observer import AgendamentoLoggingObserver
from services.observers.agendamento_email_observer import AgendamentoEmailObserver


class AgendamentoManager(Observable):
    """Manager para orquestrar operações de Agendamento"""
    
    def __init__(self):
        """
        Inicializa o manager
        """
        super().__init__()
        self.agendamento_repository = repository_factory.get_agendamento_repository()
        self.cliente_repository = repository_factory.get_cliente_repository()
        self.funcionario_repository = repository_factory.get_funcionario_repository()
        self.validacao_service = ValidacaoAgendamentoService()

        # Anexa observadores padrão
        self.attach(AgendamentoLoggingObserver())
        self.attach(AgendamentoEmailObserver())
    
    def listar_agendamentos(self):
        """
        Lista todos os agendamentos
        
        :return: lista de dicts com dados dos agendamentos
        """
        agendamentos = self.agendamento_repository.listar()
        return [agendamento.to_dict() for agendamento in agendamentos]
    
    def buscar_agendamento_por_id(self, agendamento_id):
        """
        Busca um agendamento pelo ID
        
        :param agendamento_id: ID do agendamento
        :return: dict com dados do agendamento ou None
        """
        agendamento = self.agendamento_repository.buscar_por_id(agendamento_id)
        return agendamento.to_dict() if agendamento else None
    
    def buscar_agendamentos_por_cliente(self, cliente_id):
        """
        Busca todos os agendamentos de um cliente
        
        :param cliente_id: ID do cliente
        :return: lista de dicts com dados dos agendamentos
        """
        agendamentos = self.agendamento_repository.buscar_por_cliente(cliente_id)
        return [agendamento.to_dict() for agendamento in agendamentos]
    
    def buscar_agendamentos_por_barbeiro(self, barbeiro_id):
        """
        Busca todos os agendamentos de um barbeiro
        
        :param barbeiro_id: ID do barbeiro
        :return: lista de dicts com dados dos agendamentos
        """
        agendamentos = self.agendamento_repository.buscar_por_barbeiro(barbeiro_id)
        return [agendamento.to_dict() for agendamento in agendamentos]
    
    def criar_agendamento(self, dados):
        """
        Cria um novo agendamento
        
        :param dados: dict com inicio, fim, cliente_id e barbeiro_id
        :return: dict com dados do agendamento criado
        """
        # Extração dos dados
        inicio = dados.get('inicio')
        fim = dados.get('fim')
        cliente_id = dados.get('cliente_id')
        barbeiro_id = dados.get('barbeiro_id')
        
        # Valida campos obrigatórios
        self.validacao_service.validar_dados_obrigatorios(inicio, fim, cliente_id, barbeiro_id)
        
        # Converte e valida datetime
        inicio, fim = self.validacao_service.converter_e_validar_datetime(inicio, fim)
        
        # Valida ordem dos horários
        self.validacao_service.validar_ordem_horarios(inicio, fim)
        
        # Busca e valida cliente
        cliente = self.cliente_repository.buscar_por_id(cliente_id)
        self.validacao_service.validar_cliente_existe(cliente)
        
        # Busca e valida funcionário
        funcionario = self.funcionario_repository.buscar_por_id(barbeiro_id)
        self.validacao_service.validar_barbeiro_existe_e_eh_barbeiro(funcionario)
        
        # Busca agendamentos do barbeiro e valida conflitos
        agendamentos_barbeiro = self.agendamento_repository.buscar_por_barbeiro(barbeiro_id)
        self.validacao_service.validar_conflito_horarios(barbeiro_id, inicio, fim, agendamentos_barbeiro)
        
        # Cria o agendamento
        agendamento = Agendamento(
            inicio=inicio,
            fim=fim,
            cliente_id=cliente_id,
            barbeiro_id=barbeiro_id
        )
        
        # Persiste
        agendamento_id = self.agendamento_repository.criar(agendamento)
        agendamento.id = agendamento_id
        
        dados_resultado = agendamento.to_dict()
        
        # Notifica observadores
        self.notify("agendamento_criado", dados_resultado)
        
        return dados_resultado
    
    def atualizar_agendamento(self, agendamento_id, dados):
        """
        Atualiza um agendamento existente
        
        :param agendamento_id: ID do agendamento
        :param dados: dict com campos a atualizar
        :return: dict com dados do agendamento atualizado
        """
        # Busca agendamento existente
        agendamento_existente = self.agendamento_repository.buscar_por_id(agendamento_id)
        if not agendamento_existente:
            raise NotFoundException("Agendamento não encontrado")
        
        # Extração dos dados (usa valores existentes se não fornecidos)
        inicio = dados.get('inicio', agendamento_existente.inicio)
        fim = dados.get('fim', agendamento_existente.fim)
        cliente_id = dados.get('cliente_id', agendamento_existente.cliente_id)
        barbeiro_id = dados.get('barbeiro_id', agendamento_existente.barbeiro_id)
        
        # Converte e valida datetime
        inicio, fim = self.validacao_service.converter_e_validar_datetime(inicio, fim)
        
        # Valida ordem dos horários
        self.validacao_service.validar_ordem_horarios(inicio, fim)
        
        # Valida que cliente existe (se foi alterado)
        if cliente_id != agendamento_existente.cliente_id:
            cliente = self.cliente_repository.buscar_por_id(cliente_id)
            self.validacao_service.validar_cliente_existe(cliente)
        
        # Valida que funcionário existe e é barbeiro (se foi alterado)
        if barbeiro_id != agendamento_existente.barbeiro_id:
            funcionario = self.funcionario_repository.buscar_por_id(barbeiro_id)
            self.validacao_service.validar_barbeiro_existe_e_eh_barbeiro(funcionario)
        
        # Busca agendamentos do barbeiro e valida conflitos (ignora o agendamento atual)
        agendamentos_barbeiro = self.agendamento_repository.buscar_por_barbeiro(barbeiro_id)
        self.validacao_service.validar_conflito_horarios(
            barbeiro_id, inicio, fim, agendamentos_barbeiro, agendamento_id_atual=agendamento_id
        )
        
        # Atualiza o agendamento
        agendamento = Agendamento(
            id=agendamento_id,
            inicio=inicio,
            fim=fim,
            cliente_id=cliente_id,
            barbeiro_id=barbeiro_id
        )
        
        self.agendamento_repository.atualizar(agendamento)
        
        dados_resultado = agendamento.to_dict()

        # Notifica observadores
        self.notify("agendamento_atualizado", dados_resultado)
        
        return dados_resultado
    
    def deletar_agendamento(self, agendamento_id):
        """
        Deleta um agendamento
        
        :param agendamento_id: ID do agendamento
        :return: bool indicando sucesso
        """
        agendamento = self.agendamento_repository.buscar_por_id(agendamento_id)
        if not agendamento:
            return False
            
        dados_agendamento = agendamento.to_dict()
        sucesso = self.agendamento_repository.deletar(agendamento_id)
        
        if sucesso:
            self.notify("agendamento_deletado", dados_agendamento)
            
        return sucesso
    
    def contar_agendamentos(self):
        """
        Conta o número total de agendamentos
        
        :return: int com a quantidade de agendamentos
        """
        return self.agendamento_repository.contar()


# Instância singleton
agendamento_manager = AgendamentoManager()
