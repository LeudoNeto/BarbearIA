from abc import ABC, abstractmethod

from managers.estatisticas_acesso_manager import estatisticas_acesso_manager


class RelatorioAcessosTemplate(ABC):
    """Template Method para geracao de relatorios de acessos."""

    def __init__(self, estatisticas_manager=None):
        self.estatisticas_manager = estatisticas_manager or estatisticas_acesso_manager

    def gerar_relatorio(self):
        """
        Executa o fluxo padrao de geracao do relatorio.

        :return: saida final do relatorio no formato concreto
        """
        dados_brutos = self.buscar_dados_brutos()
        estatisticas = self.calcular_estatisticas(dados_brutos)
        cabecalho = self.montar_cabecalho(estatisticas)
        corpo = self.montar_corpo(estatisticas)
        rodape = self.montar_rodape(estatisticas)
        return self.gerar_saida_final(cabecalho, corpo, rodape, estatisticas)

    def buscar_dados_brutos(self):
        """Busca o historico bruto de acessos."""
        return self.estatisticas_manager.listar_acessos_brutos()

    def calcular_estatisticas(self, dados_brutos):
        """Calcula as estatisticas agregadas para o relatorio."""
        return self.estatisticas_manager.consolidar_estatisticas(dados_brutos)

    @abstractmethod
    def montar_cabecalho(self, estatisticas):
        """Monta o cabecalho do relatorio."""

    @abstractmethod
    def montar_corpo(self, estatisticas):
        """Monta o corpo do relatorio."""

    @abstractmethod
    def montar_rodape(self, estatisticas):
        """Monta o rodape do relatorio."""

    @abstractmethod
    def gerar_saida_final(self, cabecalho, corpo, rodape, estatisticas):
        """Gera a saida final do relatorio no formato concreto."""
