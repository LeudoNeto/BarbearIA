from fastapi import APIRouter
from managers.agendamento_manager import agendamento_manager


class AgendamentoController:
    """Controller para rotas de Agendamento"""
    
    def __init__(self):
        """
        Inicializa o controller
        """
        self.agendamento_manager = agendamento_manager
        self.router = APIRouter(prefix='/agendamentos', tags=['Agendamentos'])
        self._registrar_rotas()
    
    def _registrar_rotas(self):
        """Registra as rotas do controller"""
        
        @self.router.get('')
        async def listar_agendamentos():
            """Lista todos os agendamentos"""
            return self.agendamento_manager.listar_agendamentos()
        
        @self.router.get('/{agendamento_id}')
        async def buscar_agendamento(agendamento_id: int):
            """Busca um agendamento pelo ID"""
            return self.agendamento_manager.buscar_agendamento_por_id(agendamento_id)
        
        @self.router.get('/cliente/{cliente_id}')
        async def buscar_agendamentos_por_cliente(cliente_id: int):
            """Busca todos os agendamentos de um cliente"""
            return self.agendamento_manager.buscar_agendamentos_por_cliente(cliente_id)
        
        @self.router.get('/barbeiro/{barbeiro_id}')
        async def buscar_agendamentos_por_barbeiro(barbeiro_id: int):
            """Busca todos os agendamentos de um barbeiro"""
            return self.agendamento_manager.buscar_agendamentos_por_barbeiro(barbeiro_id)
        
        @self.router.post('', status_code=201)
        async def criar_agendamento(dados: dict):
            """
            Cria um novo agendamento
            
            Espera um JSON com:
            - inicio: string (ISO 8601 datetime)
            - fim: string (ISO 8601 datetime)
            - cliente_id: int
            - barbeiro_id: int
            """
            return self.agendamento_manager.criar_agendamento(dados)
        
        @self.router.put('/{agendamento_id}')
        async def atualizar_agendamento(agendamento_id: int, dados: dict):
            """
            Atualiza um agendamento existente
            
            Espera um JSON com os campos a atualizar:
            - inicio: string (ISO 8601 datetime) - opcional
            - fim: string (ISO 8601 datetime) - opcional
            - cliente_id: int - opcional
            - barbeiro_id: int - opcional
            """
            return self.agendamento_manager.atualizar_agendamento(agendamento_id, dados)
        
        @self.router.delete('/{agendamento_id}')
        async def deletar_agendamento(agendamento_id: int):
            """Deleta um agendamento"""
            self.agendamento_manager.deletar_agendamento(agendamento_id)
            return {"message": "Agendamento deletado com sucesso"}


# Instância singleton
agendamento_controller = AgendamentoController()
