from fastapi import APIRouter, Response
from managers.horario_funcionamento_manager import horario_funcionamento_manager


class HorarioFuncionamentoController:
    """Controller para rotas de HorarioFuncionamento"""

    def __init__(self):
        """
        Inicializa o controller
        """
        self.horario_funcionamento_manager = horario_funcionamento_manager
        self.router = APIRouter(prefix='/horarios-funcionamento', tags=['Horários de Funcionamento'])
        self._registrar_rotas()

    def _registrar_rotas(self):
        """Registra as rotas do controller"""

        @self.router.get('')
        async def listar_horarios():
            """Lista todos os horários de funcionamento"""
            return self.horario_funcionamento_manager.listar_horarios()

        @self.router.post('', status_code=201)
        async def criar_horario(dados: dict):
            """Cria um novo horário de funcionamento"""
            return self.horario_funcionamento_manager.criar_horario(dados)

        @self.router.put('/{id}')
        async def atualizar_horario(id: int, dados: dict):
            """Atualiza um horário de funcionamento existente"""
            return self.horario_funcionamento_manager.atualizar_horario(id, dados)

        @self.router.delete('/{id}', status_code=204)
        async def deletar_horario(id: int):
            """Remove um horário de funcionamento"""
            self.horario_funcionamento_manager.deletar_horario(id)
            return Response(status_code=204)


# Instância singleton
horario_funcionamento_controller = HorarioFuncionamentoController()
