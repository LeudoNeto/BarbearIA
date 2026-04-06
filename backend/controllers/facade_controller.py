"""
FacadeSingletonController - Facade + Singleton refatorado para usar o padrão Command.

Cada método agora instancia o Command correspondente e delega
a execução ao CommandInvoker, eliminando chamadas diretas aos managers.
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

from commands import (
    command_invoker,
    # Auth
    LoginCommand, SignupCommand, ObterUsuarioLogadoCommand, LogoutCommand,
    # Cliente
    ListarClientesCommand, CriarClienteCommand, ContarClientesCommand,
    # Funcionário
    ListarFuncionariosCommand, CriarFuncionarioCommand, ContarFuncionariosCommand,
    # Empresa
    BuscarEmpresaCommand, AtualizarEmpresaCommand, DesfazerAtualizacaoEmpresaCommand,
    # Horário
    ListarHorariosCommand, CriarHorarioCommand, AtualizarHorarioCommand, DeletarHorarioCommand,
    # Agendamento
    ListarAgendamentosCommand, BuscarAgendamentoPorIdCommand,
    BuscarAgendamentosPorClienteCommand, BuscarAgendamentosPorBarbeiroCommand,
    CriarAgendamentoCommand, AtualizarAgendamentoCommand,
    ConfirmarAgendamentoCommand, CancelarAgendamentoCommand,
    ConcluirAgendamentoCommand, DeletarAgendamentoCommand, ContarAgendamentosCommand,
    # Estatísticas
    ObterEstatisticasSistemaCommand, ObterEstatisticasAcessoCommand,
    GerarRelatorioAcessosHtmlCommand, GerarRelatorioAcessosPdfCommand,
    # Preview
    GerarPreviewCorteCommand,
)


class FacadeSingletonController:
    """
    Facade Singleton Controller — agora delega todas as operações
    ao CommandInvoker via objetos Command, mantendo baixo acoplamento
    e permitindo extensão sem modificação desta classe.
    """

    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if FacadeSingletonController._initialized:
            return

        # Referências aos managers (apenas para passagem aos Commands)
        self._auth_manager = auth_manager
        self._cliente_manager = cliente_manager
        self._funcionario_manager = funcionario_manager
        self._empresa_manager = empresa_manager
        self._horario_manager = horario_funcionamento_manager
        self._agendamento_manager = agendamento_manager
        self._estatisticas_acesso_manager = estatisticas_acesso_manager
        self._preview_corte_manager = preview_corte_manager
        self._relatorio_acesso_manager = relatorio_acesso_manager

        # Invoker compartilhado
        self._invoker = command_invoker

        FacadeSingletonController._initialized = True

    # ==================== AUTH ====================

    def login(self, dados: dict):
        return self._invoker.executar(
            LoginCommand(self._auth_manager, dados)
        )

    def signup(self, dados: dict):
        return self._invoker.executar(
            SignupCommand(self._auth_manager, dados)
        )

    def obter_usuario_logado(self, session_id: str):
        return self._invoker.executar(
            ObterUsuarioLogadoCommand(self._auth_manager, session_id)
        )

    def logout(self, session_id: str):
        return self._invoker.executar(
            LogoutCommand(self._auth_manager, session_id)
        )

    # ==================== CLIENTE ====================

    def listar_clientes(self):
        return self._invoker.executar(
            ListarClientesCommand(self._cliente_manager)
        )

    def criar_cliente(self, dados: dict):
        return self._invoker.executar(
            CriarClienteCommand(self._cliente_manager, dados)
        )

    # ==================== FUNCIONARIO ====================

    def listar_funcionarios(self):
        return self._invoker.executar(
            ListarFuncionariosCommand(self._funcionario_manager)
        )

    def criar_funcionario(self, dados: dict):
        return self._invoker.executar(
            CriarFuncionarioCommand(self._funcionario_manager, dados)
        )

    # ==================== EMPRESA ====================

    def buscar_empresa(self):
        return self._invoker.executar(
            BuscarEmpresaCommand(self._empresa_manager)
        )

    def atualizar_empresa(self, dados: dict):
        return self._invoker.executar(
            AtualizarEmpresaCommand(self._empresa_manager, dados)
        )

    def desfazer_ultima_atualizacao_empresa(self):
        return self._invoker.executar(
            DesfazerAtualizacaoEmpresaCommand(self._empresa_manager)
        )

    # ==================== HORARIO FUNCIONAMENTO ====================

    def listar_horarios_funcionamento(self):
        return self._invoker.executar(
            ListarHorariosCommand(self._horario_manager)
        )

    def criar_horario_funcionamento(self, dados: dict):
        return self._invoker.executar(
            CriarHorarioCommand(self._horario_manager, dados)
        )

    def atualizar_horario_funcionamento(self, horario_id: int, dados: dict):
        return self._invoker.executar(
            AtualizarHorarioCommand(self._horario_manager, horario_id, dados)
        )

    def deletar_horario_funcionamento(self, horario_id: int):
        return self._invoker.executar(
            DeletarHorarioCommand(self._horario_manager, horario_id)
        )

    # ==================== AGENDAMENTO ====================

    def listar_agendamentos(self):
        return self._invoker.executar(
            ListarAgendamentosCommand(self._agendamento_manager)
        )

    def buscar_agendamento_por_id(self, agendamento_id: int):
        return self._invoker.executar(
            BuscarAgendamentoPorIdCommand(self._agendamento_manager, agendamento_id)
        )

    def buscar_agendamentos_por_cliente(self, cliente_id: int):
        return self._invoker.executar(
            BuscarAgendamentosPorClienteCommand(self._agendamento_manager, cliente_id)
        )

    def buscar_agendamentos_por_barbeiro(self, barbeiro_id: int):
        return self._invoker.executar(
            BuscarAgendamentosPorBarbeiroCommand(self._agendamento_manager, barbeiro_id)
        )

    def criar_agendamento(self, dados: dict):
        return self._invoker.executar(
            CriarAgendamentoCommand(self._agendamento_manager, dados)
        )

    def atualizar_agendamento(self, agendamento_id: int, dados: dict):
        return self._invoker.executar(
            AtualizarAgendamentoCommand(self._agendamento_manager, agendamento_id, dados)
        )

    def confirmar_agendamento(self, agendamento_id: int):
        return self._invoker.executar(
            ConfirmarAgendamentoCommand(self._agendamento_manager, agendamento_id)
        )

    def cancelar_agendamento(self, agendamento_id: int):
        return self._invoker.executar(
            CancelarAgendamentoCommand(self._agendamento_manager, agendamento_id)
        )

    def concluir_agendamento(self, agendamento_id: int):
        return self._invoker.executar(
            ConcluirAgendamentoCommand(self._agendamento_manager, agendamento_id)
        )

    def deletar_agendamento(self, agendamento_id: int):
        return self._invoker.executar(
            DeletarAgendamentoCommand(self._agendamento_manager, agendamento_id)
        )

    # ==================== ESTATISTICAS ====================

    def obter_estatisticas_sistema(self):
        return self._invoker.executar(
            ObterEstatisticasSistemaCommand(
                self._cliente_manager,
                self._funcionario_manager,
                self._agendamento_manager,
            )
        )

    def obter_estatisticas_acesso(self):
        return self._invoker.executar(
            ObterEstatisticasAcessoCommand(self._estatisticas_acesso_manager)
        )

    def gerar_relatorio_acessos_html(self):
        return self._invoker.executar(
            GerarRelatorioAcessosHtmlCommand(self._relatorio_acesso_manager)
        )

    def gerar_relatorio_acessos_pdf(self):
        return self._invoker.executar(
            GerarRelatorioAcessosPdfCommand(self._relatorio_acesso_manager)
        )

    # ==================== PREVIEW CORTE ====================

    def gerar_preview_corte(
        self,
        imagem_pessoa_bytes: bytes,
        imagem_corte_bytes: bytes,
        usar_mock: bool = False,
    ):
        return self._invoker.executar(
            GerarPreviewCorteCommand(
                self._preview_corte_manager,
                imagem_pessoa_bytes,
                imagem_corte_bytes,
                usar_mock,
            )
        )

    # ==================== UTILITÁRIOS ====================

    def obter_historico_comandos(self) -> list[dict]:
        """Expõe o histórico de execuções de comandos para auditoria."""
        return self._invoker.obter_historico()


facade_controller = FacadeSingletonController()