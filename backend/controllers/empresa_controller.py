from fastapi import APIRouter
from controllers.facade_controller import facade_controller


class EmpresaController:
    """Controller para rotas de Empresa"""

    def __init__(self):
        """
        Inicializa o controller
        """
        self.facade = facade_controller
        self.router = APIRouter(prefix='/empresa', tags=['Empresa'])
        self._registrar_rotas()

    def _registrar_rotas(self):
        """Registra as rotas do controller"""

        @self.router.get('')
        async def buscar_empresa():
            """Retorna os dados da empresa"""
            return self.facade.buscar_empresa()

        @self.router.put('')
        async def atualizar_empresa(dados: dict):
            """Atualiza os dados da empresa"""
            return self.facade.atualizar_empresa(dados)

        @self.router.post('/desfazer-ultima-atualizacao')
        async def desfazer_ultima_atualizacao_empresa():
            """Desfaz a última atualização dos dados da empresa"""
            return self.facade.desfazer_ultima_atualizacao_empresa()


# Instância singleton
empresa_controller = EmpresaController()
