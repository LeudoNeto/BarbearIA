from fastapi import APIRouter, File, Form, UploadFile
from controllers.facade_controller import facade_controller


class PreviewCorteController:
    """Controller para geração de preview de corte com IA."""

    def __init__(self):
        """
        Inicializa o controller.
        """
        self.facade = facade_controller
        self.router = APIRouter(prefix='/preview-corte', tags=['Preview Corte'])
        self._registrar_rotas()

    def _registrar_rotas(self):
        """Registra as rotas do controller."""

        @self.router.post('')
        async def gerar_preview_corte(
            imagem_pessoa: UploadFile = File(...),
            imagem_corte: UploadFile = File(...),
            usar_mock: bool = Form(False)
        ):
            """
            Gera preview de corte com base na imagem da pessoa e na imagem de referência.

            Campos esperados em multipart/form-data:
            - imagem_pessoa: arquivo da foto da pessoa
            - imagem_corte: arquivo da foto do corte desejado
            - usar_mock: bool opcional para forçar strategy mockada (padrão: false)
            """
            imagem_pessoa_bytes = await imagem_pessoa.read()
            imagem_corte_bytes = await imagem_corte.read()

            return self.facade.gerar_preview_corte(
                imagem_pessoa_bytes=imagem_pessoa_bytes,
                imagem_corte_bytes=imagem_corte_bytes,
                usar_mock=usar_mock
            )


# Instância singleton
preview_corte_controller = PreviewCorteController()
