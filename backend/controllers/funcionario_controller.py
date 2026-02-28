from fastapi import APIRouter
from controllers.facade_controller import facade_controller


class FuncionarioController:
    """Controller para rotas de Funcionario"""
    
    def __init__(self):
        """
        Inicializa o controller
        """
        self.facade = facade_controller
        self.router = APIRouter(prefix='/funcionarios', tags=['Funcionarios'])
        self._registrar_rotas()
    
    def _registrar_rotas(self):
        """Registra as rotas do controller"""
        
        @self.router.get('')
        async def listar_funcionarios():
            """Lista todos os funcionários"""
            return self.facade.listar_funcionarios()
        
        @self.router.post('', status_code=201)
        async def criar_funcionario(dados: dict):
            """Cria um novo funcionário"""
            return self.facade.criar_funcionario(dados)


# Instância singleton
funcionario_controller = FuncionarioController()
