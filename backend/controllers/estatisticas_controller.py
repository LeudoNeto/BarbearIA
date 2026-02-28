from fastapi import APIRouter
from controllers.facade_controller import facade_controller


class EstatisticasController:
    """Controller para estatísticas do sistema"""
    
    def __init__(self):
        """
        Inicializa o controller
        """
        self.facade = facade_controller
        self.router = APIRouter(prefix='/estatisticas', tags=['Estatísticas'])
        self._registrar_rotas()
    
    def _registrar_rotas(self):
        """Registra as rotas do controller"""
        
        @self.router.get('')
        async def obter_estatisticas():
            """
            Obtém estatísticas gerais do sistema
            
            Retorna a quantidade de entidades (linhas) em cada tabela do banco de dados:
            - clientes: número total de clientes cadastrados
            - funcionarios: número total de funcionários cadastrados
            - agendamentos: número total de agendamentos no sistema
            """
            return self.facade.obter_estatisticas_sistema()


# Instância singleton
estatisticas_controller = EstatisticasController()
