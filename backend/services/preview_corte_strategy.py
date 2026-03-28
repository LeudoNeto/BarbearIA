"""
Strategies para geração de preview de corte.
"""
import os
from abc import ABC, abstractmethod
from uuid import uuid4
from exceptions import ValidationException
from services.preview_corte_adapter import OpenAIImageAdapter


class PreviewCorteStrategy(ABC):
    """Interface Strategy para geração de preview de corte."""

    @abstractmethod
    def gerar_preview(self, imagem_pessoa_bytes: bytes, imagem_corte_bytes: bytes) -> str:
        """Gera preview e retorna o caminho da imagem gerada."""


class OpenAIPreviewCorteStrategy(PreviewCorteStrategy):
    """Strategy concreta que usa OpenAI para gerar preview real."""

    def __init__(self, adapter: OpenAIImageAdapter, diretorio_saida: str):
        """
        Inicializa strategy da OpenAI.

        :param adapter: Adapter da OpenAI
        :param diretorio_saida: Diretório absoluto para salvar previews gerados
        """
        self.adapter = adapter
        self.diretorio_saida = diretorio_saida

    def gerar_preview(self, imagem_pessoa_bytes: bytes, imagem_corte_bytes: bytes) -> str:
        """
        Gera preview real usando OpenAI e persiste em arquivo.

        :return: caminho relativo da imagem gerada
        """
        if not imagem_pessoa_bytes:
            raise ValidationException("A imagem da pessoa é obrigatória")

        if not imagem_corte_bytes:
            raise ValidationException("A imagem de referência do corte é obrigatória")

        prompt = """
        Apply the hairstyle from the second image to the person in the first image.
        Keep the person's face identical.
        Make it photorealistic.
        """

        imagem_gerada_bytes = self.adapter.editar_imagem(
            imagem_pessoa_bytes=imagem_pessoa_bytes,
            imagem_corte_bytes=imagem_corte_bytes,
            prompt=prompt,
            tamanho="1024x1024"
        )

        os.makedirs(self.diretorio_saida, exist_ok=True)
        nome_arquivo = f"preview_corte_{uuid4().hex}.png"
        caminho_arquivo = os.path.join(self.diretorio_saida, nome_arquivo)

        with open(caminho_arquivo, "wb") as arquivo:
            arquivo.write(imagem_gerada_bytes)

        return os.path.join("backend", "generated_previews", nome_arquivo)


class MockPreviewCorteStrategy(PreviewCorteStrategy):
    """Strategy mockada para testes sem integração externa."""

    def gerar_preview(self, imagem_pessoa_bytes: bytes, imagem_corte_bytes: bytes) -> str:
        """Retorna preview fixo para testes."""
        return "backend\\preview_corte_default.png"
