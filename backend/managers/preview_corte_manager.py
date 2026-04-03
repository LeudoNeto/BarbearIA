import os
import shutil
from config.preview import preview_config
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
        self.diretorio_previews = preview_config.preview_static_dir
        self.preview_public_base_url = preview_config.preview_base_url

        os.makedirs(self.diretorio_previews, exist_ok=True)
        self._garantir_preview_default()

        self.mock_strategy = MockPreviewCorteStrategy(
            preview_public_base_url=self.preview_public_base_url
        )
        self.openai_strategy = self._criar_openai_strategy()

    def _garantir_preview_default(self):
        """
        Garante que o preview padrão exista na pasta estática de previews.
        """
        destino_default = preview_config.preview_default_path
        if os.path.exists(destino_default):
            return

        origem_legada = preview_config.preview_default_legacy_path
        if os.path.exists(origem_legada):
            shutil.copyfile(origem_legada, destino_default)

    def _criar_openai_strategy(self):
        """
        Cria strategy da OpenAI se houver API key configurada.
        """
        api_key = preview_config.openai_api_key
        if not api_key:
            return None

        adapter = OpenAIImageAdapter(api_key=api_key)
        return OpenAIPreviewCorteStrategy(
            adapter=adapter,
            diretorio_saida=self.diretorio_previews,
            preview_public_base_url=self.preview_public_base_url
        )

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
