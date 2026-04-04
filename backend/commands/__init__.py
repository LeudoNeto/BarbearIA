from .base_command import Command
from .command_invoker import CommandInvoker, command_invoker
from .agendamento_commands import (
    ListarAgendamentosCommand,
    BuscarAgendamentoPorIdCommand,
    BuscarAgendamentosPorClienteCommand,
    BuscarAgendamentosPorBarbeiroCommand,
    CriarAgendamentoCommand,
    AtualizarAgendamentoCommand,
    DeletarAgendamentoCommand,
    ContarAgendamentosCommand,
)
from .auth_commands import (
    LoginCommand,
    SignupCommand,
    ObterUsuarioLogadoCommand,
    LogoutCommand,
)
from .cliente_commands import (
    ListarClientesCommand,
    CriarClienteCommand,
    ContarClientesCommand,
)
from .empresa_commands import (
    BuscarEmpresaCommand,
    AtualizarEmpresaCommand,
    DesfazerAtualizacaoEmpresaCommand,
)
from .estatisticas_commands import (
    ObterEstatisticasSistemaCommand,
    ObterEstatisticasAcessoCommand,
    GerarRelatorioAcessosHtmlCommand,
    GerarRelatorioAcessosPdfCommand,
)
from .funcionario_commands import (
    ListarFuncionariosCommand,
    CriarFuncionarioCommand,
    ContarFuncionariosCommand,
)
from .horario_funcionamento_commands import (
    ListarHorariosCommand,
    CriarHorarioCommand,
    AtualizarHorarioCommand,
    DeletarHorarioCommand,
)
from .preview_corte_commands import GerarPreviewCorteCommand

__all__ = [
    "Command",
    "CommandInvoker",
    "command_invoker",
    "LoginCommand", "SignupCommand", "ObterUsuarioLogadoCommand", "LogoutCommand",
    "ListarClientesCommand", "CriarClienteCommand", "ContarClientesCommand",
    "ListarFuncionariosCommand", "CriarFuncionarioCommand", "ContarFuncionariosCommand",
    "BuscarEmpresaCommand", "AtualizarEmpresaCommand", "DesfazerAtualizacaoEmpresaCommand",
    "ListarHorariosCommand", "CriarHorarioCommand", "AtualizarHorarioCommand", "DeletarHorarioCommand",
    "ListarAgendamentosCommand", "BuscarAgendamentoPorIdCommand",
    "BuscarAgendamentosPorClienteCommand", "BuscarAgendamentosPorBarbeiroCommand",
    "CriarAgendamentoCommand", "AtualizarAgendamentoCommand",
    "DeletarAgendamentoCommand", "ContarAgendamentosCommand",
    "ObterEstatisticasSistemaCommand", "ObterEstatisticasAcessoCommand",
    "GerarRelatorioAcessosHtmlCommand", "GerarRelatorioAcessosPdfCommand",
    "GerarPreviewCorteCommand",
]