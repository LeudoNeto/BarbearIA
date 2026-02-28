from exceptions import DuplicateException, NotFoundException


class HorarioFuncionamentoMemoryRepository:
    """Repositório em memória para operações de persistência de HorarioFuncionamento"""

    def __init__(self):
        """
        Inicializa o repositório em memória
        """
        self._horarios = {}  # Dicionário id -> HorarioFuncionamento
        self._next_id = 1

    def listar(self):
        """
        Lista todos os horários de funcionamento ordenados por dia da semana

        :return: Lista de objetos HorarioFuncionamento
        """
        return sorted(self._horarios.values(), key=lambda h: h.dia_semana)

    def buscar_por_id(self, id):
        """
        Busca um horário de funcionamento pelo ID

        :param id: ID do horário
        :return: Objeto HorarioFuncionamento
        :raises NotFoundException: se o horário não for encontrado
        """
        if id not in self._horarios:
            raise NotFoundException("Horário de funcionamento não encontrado")
        return self._horarios[id]

    def listar_por_dia(self, dia_semana, id_excluir=None):
        """
        Lista horários de um dia específico, opcionalmente excluindo um registro pelo ID

        :param dia_semana: dia da semana (0-6)
        :param id_excluir: ID a ser ignorado na busca (para validação de atualização)
        :return: Lista de objetos HorarioFuncionamento
        """
        return [
            h for h in self._horarios.values()
            if h.dia_semana == dia_semana and (id_excluir is None or h.id != id_excluir)
        ]

    def criar(self, horario):
        """
        Cria um novo horário de funcionamento em memória

        :param horario: Objeto HorarioFuncionamento
        :return: ID do horário criado
        """
        # Verifica se já existe horário para o dia
        for existing in self._horarios.values():
            if existing.dia_semana == horario.dia_semana:
                raise DuplicateException("Já existe um horário cadastrado para este dia da semana")

        horario.id = self._next_id
        self._horarios[self._next_id] = horario
        self._next_id += 1

        return horario.id

    def atualizar(self, horario):
        """
        Atualiza um horário de funcionamento em memória

        :param horario: Objeto HorarioFuncionamento com os dados atualizados
        :return: Objeto HorarioFuncionamento atualizado
        :raises NotFoundException: se o horário não for encontrado
        """
        if horario.id not in self._horarios:
            raise NotFoundException("Horário de funcionamento não encontrado")

        # Verifica conflito de dia (excluindo o próprio registro)
        for existing in self._horarios.values():
            if existing.dia_semana == horario.dia_semana and existing.id != horario.id:
                raise DuplicateException("Já existe um horário cadastrado para este dia da semana")

        self._horarios[horario.id] = horario
        return horario

    def deletar(self, id):
        """
        Remove um horário de funcionamento pelo ID

        :param id: ID do horário a ser removido
        :raises NotFoundException: se o horário não for encontrado
        """
        if id not in self._horarios:
            raise NotFoundException("Horário de funcionamento não encontrado")

        del self._horarios[id]


# Instância singleton
horario_funcionamento_memory_repository = HorarioFuncionamentoMemoryRepository()
