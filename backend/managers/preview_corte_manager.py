import os
from exceptions import ValidationException
from services.preview_corte_adapter import OpenAIImageAdapter
from services.preview_corte_strategy import (
    MockPreviewCorteStrategy,
    OpenAIPreviewCorteStrategy,
    PreviewCorteStrategy
)


class PreviewCorteManager:
    """Manager para orquestrar geração de preview de corte com Strategy."""

    def __init__(self):
        """
        Inicializa o manager e prepara as strategies disponíveis.
        """
        self.mock_strategy = MockPreviewCorteStrategy()
        self.openai_strategy = self._criar_openai_strategy()

    def _criar_openai_strategy(self):
        """
        Cria strategy da OpenAI se houver API key configurada.
        """
        api_key = os.getenv("OPENAI_API_KEY") or os.getenv("OPENAPI_API_KEY")
        if not api_key:
            return None

        diretorio_backend = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        diretorio_saida = os.path.join(diretorio_backend, "generated_previews")

        adapter = OpenAIImageAdapter(api_key=api_key)
        return OpenAIPreviewCorteStrategy(adapter=adapter, diretorio_saida=diretorio_saida)

    def _selecionar_strategy(self, usar_mock: bool) -> PreviewCorteStrategy:
        """
        Seleciona a strategy de geração conforme o cenário.
        """
        if usar_mock:
            return self.mock_strategy

        if not self.openai_strategy:
            raise ValidationException(
                "A chave da OpenAI não está configurada. Configure OPENAI_API_KEY para usar preview real."
            )

        return self.openai_strategy

    def gerar_preview_corte(self, imagem_pessoa_bytes: bytes, imagem_corte_bytes: bytes, usar_mock: bool = False):
        """
        Gera preview de corte e retorna dados da execução.

        :param imagem_pessoa_bytes: bytes da foto da pessoa
        :param imagem_corte_bytes: bytes da foto de referência do corte
        :param usar_mock: força uso da strategy mockada
        :return: dict com caminho do preview e strategy utilizada
        """
        strategy = self._selecionar_strategy(usar_mock=usar_mock)
        preview_path = strategy.gerar_preview(
            imagem_pessoa_bytes=imagem_pessoa_bytes,
            imagem_corte_bytes=imagem_corte_bytes
        )

        return {
            "preview_path": preview_path,
            "strategy": "mock" if usar_mock else "openai"
        }


# Instância singleton
preview_corte_manager = PreviewCorteManager()
