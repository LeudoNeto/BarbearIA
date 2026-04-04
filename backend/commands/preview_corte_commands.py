"""
Commands de preview de corte com IA.
"""
from commands.base_command import Command


class GerarPreviewCorteCommand(Command):
    """Encapsula a geração de preview de corte via IA."""

    def __init__(
        self,
        preview_corte_manager,
        imagem_pessoa_bytes: bytes,
        imagem_corte_bytes: bytes,
        usar_mock: bool = False,
    ):
        self._preview_corte_manager = preview_corte_manager
        self._imagem_pessoa_bytes = imagem_pessoa_bytes
        self._imagem_corte_bytes = imagem_corte_bytes
        self._usar_mock = usar_mock

    def execute(self) -> dict:
        return self._preview_corte_manager.gerar_preview_corte(
            imagem_pessoa_bytes=self._imagem_pessoa_bytes,
            imagem_corte_bytes=self._imagem_corte_bytes,
            usar_mock=self._usar_mock,
        )