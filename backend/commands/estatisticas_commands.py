"""
Commands de estatísticas e relatórios.
"""
from commands.base_command import Command


class ObterEstatisticasSistemaCommand(Command):
    def __init__(self, cliente_manager, funcionario_manager, agendamento_manager):
        self._cliente_manager = cliente_manager
        self._funcionario_manager = funcionario_manager
        self._agendamento_manager = agendamento_manager

    def execute(self) -> dict:
        return {
            "clientes": self._cliente_manager.contar_clientes(),
            "funcionarios": self._funcionario_manager.contar_funcionarios(),
            "agendamentos": self._agendamento_manager.contar_agendamentos(),
        }


class ObterEstatisticasAcessoCommand(Command):
    def __init__(self, estatisticas_acesso_manager):
        self._manager = estatisticas_acesso_manager

    def execute(self) -> dict:
        return self._manager.obter_estatisticas_acesso()


class GerarRelatorioAcessosHtmlCommand(Command):
    def __init__(self, relatorio_acesso_manager):
        self._manager = relatorio_acesso_manager

    def execute(self) -> str:
        return self._manager.gerar_relatorio_acessos_html()


class GerarRelatorioAcessosPdfCommand(Command):
    def __init__(self, relatorio_acesso_manager):
        self._manager = relatorio_acesso_manager

    def execute(self) -> bytes:
        return self._manager.gerar_relatorio_acessos_pdf()