from models.horario_funcionamento import HorarioFuncionamento
from services.validacao_horario_service import ValidacaoHorarioService
from repositories.repository_factory import repository_factory


class HorarioFuncionamentoManager:
    """Manager para orquestrar operações de HorarioFuncionamento"""

    def __init__(self):
        """
        Inicializa o manager
        """
        self.horario_repository = repository_factory.get_horario_funcionamento_repository()
        self.validacao_service = ValidacaoHorarioService()

    def listar_horarios(self):
        """
        Lista todos os horários de funcionamento

        :return: lista de dicts com os horários de funcionamento
        """
        horarios = self.horario_repository.listar()
        return [horario.to_dict() for horario in horarios]

    def criar_horario(self, dados):
        """
        Cria um novo horário de funcionamento

        :param dados: dict com dia_semana, hora_inicio e hora_fim
        :return: dict com dados do horário criado
        """
        dia_semana = dados.get('dia_semana')
        hora_inicio = dados.get('hora_inicio')
        hora_fim = dados.get('hora_fim')

        # Valida os dados do horário
        self.validacao_service.validar_horario_funcionamento(dia_semana, hora_inicio, hora_fim)

        # Verifica conflito de dia da semana
        horarios_existentes = self.horario_repository.listar_por_dia(dia_semana)
        self.validacao_service.validar_conflito_horario(dia_semana, horarios_existentes)

        # Cria o horário
        horario = HorarioFuncionamento(
            dia_semana=int(dia_semana),
            hora_inicio=hora_inicio,
            hora_fim=hora_fim
        )

        horario_id = self.horario_repository.criar(horario)
        horario.id = horario_id

        return horario.to_dict()

    def atualizar_horario(self, id, dados):
        """
        Atualiza um horário de funcionamento existente

        :param id: ID do horário a ser atualizado
        :param dados: dict com os campos a atualizar (parcial ou total)
        :return: dict com os dados atualizados do horário
        """
        # Busca o horário pelo ID
        horario = self.horario_repository.buscar_por_id(id)

        # Aplica os campos fornecidos (atualização parcial)
        dia_semana = dados.get('dia_semana', horario.dia_semana)
        hora_inicio = dados.get('hora_inicio', horario.hora_inicio)
        hora_fim = dados.get('hora_fim', horario.hora_fim)

        # Valida os dados do horário
        self.validacao_service.validar_horario_funcionamento(dia_semana, hora_inicio, hora_fim)

        # Verifica conflito de dia, excluindo o próprio registro
        horarios_existentes = self.horario_repository.listar_por_dia(dia_semana, id_excluir=id)
        self.validacao_service.validar_conflito_horario(dia_semana, horarios_existentes)

        horario.dia_semana = int(dia_semana)
        horario.hora_inicio = hora_inicio
        horario.hora_fim = hora_fim

        self.horario_repository.atualizar(horario)
        return horario.to_dict()

    def deletar_horario(self, id):
        """
        Remove um horário de funcionamento pelo ID

        :param id: ID do horário a ser removido
        """
        self.horario_repository.deletar(id)


# Instância singleton
horario_funcionamento_manager = HorarioFuncionamentoManager()
