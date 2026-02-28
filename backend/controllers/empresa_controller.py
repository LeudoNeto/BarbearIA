from fastapi import APIRouter
from managers.empresa_manager import empresa_manager


class EmpresaController:
    """Controller para rotas de Empresa"""

    def __init__(self):
        """
        Inicializa o controller
        """
        self.empresa_manager = empresa_manager
        self.router = APIRouter(prefix='/empresa', tags=['Empresa'])
        self._registrar_rotas()

    def _registrar_rotas(self):
        """Registra as rotas do controller"""

        @self.router.get('')
        async def buscar_empresa():
            """Retorna os dados da empresa"""
            return self.empresa_manager.buscar_empresa()

        @self.router.put('')
        async def atualizar_empresa(dados: dict):
            """Atualiza os dados da empresa"""
            return self.empresa_manager.atualizar_empresa(dados)


# Instância singleton
empresa_controller = EmpresaController()
