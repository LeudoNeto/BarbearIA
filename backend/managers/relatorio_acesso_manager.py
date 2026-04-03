from services.relatorio_acessos_html import RelatorioAcessosHTML
from services.relatorio_acessos_pdf import RelatorioAcessosPDF


class RelatorioAcessoManager:
    """Manager para gerar relatorios de acesso em formatos diferentes."""

    def gerar_relatorio_acessos_html(self):
        """
        Gera o relatorio de acessos em HTML usando Template Method.

        :return: string HTML com o relatorio consolidado
        """
        relatorio = RelatorioAcessosHTML()
        return relatorio.gerar_relatorio()

    def gerar_relatorio_acessos_pdf(self):
        """
        Gera o relatorio de acessos em PDF usando Template Method.

        :return: bytes do PDF com o relatorio consolidado
        """
        relatorio = RelatorioAcessosPDF()
        return relatorio.gerar_relatorio()


relatorio_acesso_manager = RelatorioAcessoManager()
