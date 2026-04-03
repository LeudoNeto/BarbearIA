from fastapi import APIRouter
from fastapi import Response
from fastapi.responses import HTMLResponse

from controllers.facade_controller import facade_controller


class EstatisticasController:
    """Controller para estatisticas do sistema."""

    def __init__(self):
        """
        Inicializa o controller.
        """
        self.facade = facade_controller
        self.router = APIRouter(prefix='/estatisticas', tags=['Estatisticas'])
        self._registrar_rotas()

    def _registrar_rotas(self):
        """Registra as rotas do controller."""

        @self.router.get('')
        async def obter_estatisticas():
            """
            Obtem estatisticas gerais do sistema.

            Retorna a quantidade de entidades (linhas) em cada tabela do banco de dados:
            - clientes: numero total de clientes cadastrados
            - funcionarios: numero total de funcionarios cadastrados
            - agendamentos: numero total de agendamentos no sistema
            """
            return self.facade.obter_estatisticas_sistema()

        @self.router.get('/acessos')
        async def obter_estatisticas_acesso():
            """
            Obtem estatisticas agregadas de acesso dos usuarios.

            Retorna:
            - total_logins
            - usuarios_que_acessaram
            - ultimo_acesso_por_usuario
            - acessos_por_periodo
            - acessos_por_tipo_usuario
            """
            return self.facade.obter_estatisticas_acesso()

        @self.router.get('/acessos/relatorio-html', response_class=HTMLResponse)
        async def obter_relatorio_html_acessos():
            """
            Gera e retorna o relatorio HTML de acessos dos usuarios.
            """
            return self.facade.gerar_relatorio_acessos_html()

        @self.router.get('/acessos/relatorio-pdf')
        async def obter_relatorio_pdf_acessos():
            """
            Gera e retorna o relatorio PDF de acessos dos usuarios.
            """
            pdf_bytes = self.facade.gerar_relatorio_acessos_pdf()
            return Response(
                content=pdf_bytes,
                media_type='application/pdf',
                headers={'Content-Disposition': 'inline; filename=relatorio_acessos.pdf'}
            )


estatisticas_controller = EstatisticasController()
