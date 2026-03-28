"""
Adapter para integração com API de imagens da OpenAI.
"""
import base64
from io import BytesIO
from openai import OpenAI


class OpenAIImageAdapter:
    """Adapter para encapsular a chamada de edição de imagem da OpenAI."""

    def __init__(self, api_key: str):
        """
        Inicializa o adapter com a API key da OpenAI.

        :param api_key: Chave da API OpenAI
        """
        self.client = OpenAI(api_key=api_key)

    def editar_imagem(self, imagem_pessoa_bytes: bytes, imagem_corte_bytes: bytes, prompt: str, tamanho: str = "1024x1024") -> bytes:
        """
        Executa edição de imagem usando duas imagens de entrada.

        :param imagem_pessoa_bytes: Conteúdo da imagem da pessoa
        :param imagem_corte_bytes: Conteúdo da imagem de referência do corte
        :param prompt: Prompt para orientar a edição
        :param tamanho: Tamanho de saída da imagem
        :return: bytes da imagem gerada
        """
        imagem_pessoa = BytesIO(imagem_pessoa_bytes)
        imagem_pessoa.name = "imagem_pessoa.png"

        imagem_corte = BytesIO(imagem_corte_bytes)
        imagem_corte.name = "imagem_corte.png"

        result = self.client.images.edit(
            model="gpt-image-1.5",
            image=[imagem_pessoa, imagem_corte],
            prompt=prompt,
            size=tamanho
        )

        if not result.data or not result.data[0].b64_json:
            raise ValueError("A OpenAI não retornou imagem válida")

        return base64.b64decode(result.data[0].b64_json)
