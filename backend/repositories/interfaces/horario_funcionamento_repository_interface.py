from abc import ABC, abstractmethod
from typing import List, Optional
from models.horario_funcionamento import HorarioFuncionamento

class HorarioFuncionamentoRepositoryInterface(ABC):
    @abstractmethod
    def listar(self) -> List[HorarioFuncionamento]:
        """
        Lista todos os horários de funcionamento ordenados por dia da semana.

        :return: Lista de objetos HorarioFuncionamento
        """
        pass

    @abstractmethod
    def buscar_por_id(self, id: int) -> HorarioFuncionamento:
        """
        Busca um horário de funcionamento pelo ID.

        :param id: ID do horário
        :return: Objeto HorarioFuncionamento
        :raises NotFoundException: se o horário não for encontrado
        """
        pass

    @abstractmethod
    def listar_por_dia(self, dia_semana: int, id_excluir: Optional[int] = None) -> List[HorarioFuncionamento]:
        """
        Lista horários de um dia específico, opcionalmente excluindo um registro pelo ID.

        :param dia_semana: dia da semana (0-6)
        :param id_excluir: ID a ser ignorado na busca (para validação de atualização)
        :return: Lista de objetos HorarioFuncionamento
        """
        pass

    @abstractmethod
    def criar(self, horario: HorarioFuncionamento) -> int:
        """
        Cria um novo horário de funcionamento.

        :param horario: Objeto HorarioFuncionamento
        :return: ID do horário criado
        """
        pass

    @abstractmethod
    def atualizar(self, horario: HorarioFuncionamento) -> HorarioFuncionamento:
        """
        Atualiza um horário de funcionamento existente.

        :param horario: Objeto HorarioFuncionamento com os dados atualizados
        :return: Objeto HorarioFuncionamento atualizado
        :raises NotFoundException: se o horário não for encontrado
        """
        pass

    @abstractmethod
    def deletar(self, id: int) -> None:
        """
        Remove um horário de funcionamento pelo ID.

        :param id: ID do horário a ser removido
        :raises NotFoundException: se o horário não for encontrado
        """
        pass
