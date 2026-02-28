from fastapi import APIRouter
from controllers.facade_controller import facade_controller


class ClienteController:
    """Controller para rotas de Cliente"""
    
    def __init__(self):
        """
        Inicializa o controller
        """
        self.facade = facade_controller
        self.router = APIRouter(prefix='/clientes', tags=['Clientes'])
        self._registrar_rotas()
    
    def _registrar_rotas(self):
        """Registra as rotas do controller"""
        
        @self.router.get('')
        async def listar_clientes():
            """Lista todos os clientes"""
            return self.facade.listar_clientes()
        
        @self.router.post('', status_code=201)
        async def criar_cliente(dados: dict):
            """Cria um novo cliente"""
            return self.facade.criar_cliente(dados)


# Instância singleton
cliente_controller = ClienteController()
