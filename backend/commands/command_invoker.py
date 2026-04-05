"""
CommandInvoker - Responsável por despachar, logar e executar comandos.
Suporta histórico de execuções para fins de auditoria e depuração.
"""
import logging
from datetime import datetime
from typing import Any

from commands.base_command import Command

logger = logging.getLogger(__name__)


class CommandInvoker:
    """
    Despachante de comandos. Centraliza a execução de todos os Commands,
    adicionando suporte a log, histórico e tratamento de erros uniforme.

    Implementado como Singleton para manter histórico global de execuções.
    """

    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if CommandInvoker._initialized:
            return
        self._historico: list[dict] = []
        CommandInvoker._initialized = True

    def executar(self, command: Command) -> Any:
        """
        Executa um comando, registrando log e histórico da operação.

        :param command: instância de Command a executar
        :return: resultado retornado pelo comando
        :raises Exception: repropaga qualquer exceção ocorrida na execução
        """
        nome_comando = type(command).__name__
        inicio = datetime.now()

        logger.info(f"[CommandInvoker] Executando: {nome_comando}")

        try:
            resultado = command.execute()

            entrada = {
                "comando": nome_comando,
                "inicio": inicio.isoformat(),
                "fim": datetime.now().isoformat(),
                "status": "sucesso",
            }
            self._historico.append(entrada)

            logger.info(f"[CommandInvoker] Concluído com sucesso: {nome_comando}")
            return resultado

        except Exception as erro:
            entrada = {
                "comando": nome_comando,
                "inicio": inicio.isoformat(),
                "fim": datetime.now().isoformat(),
                "status": "erro",
                "erro": str(erro),
            }
            self._historico.append(entrada)

            logger.error(
                f"[CommandInvoker] Erro ao executar {nome_comando}: {erro}",
                exc_info=True,
            )
            raise

    def obter_historico(self) -> list[dict]:
        """
        Retorna o histórico completo de execuções de comandos.

        :return: lista de registros de execução
        """
        return list(self._historico)

    def limpar_historico(self) -> None:
        """Remove todos os registros do histórico."""
        self._historico.clear()


# Instância singleton
command_invoker = CommandInvoker()