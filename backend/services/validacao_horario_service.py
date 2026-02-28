from datetime import datetime
from exceptions import ValidationException
from models.horario_funcionamento import HorarioFuncionamento


class ValidacaoHorarioService:
    """Service para validação de dados de horários de funcionamento"""

    def validar_horario_funcionamento(self, dia_semana, hora_inicio: str, hora_fim: str) -> None:
        """
        Valida os dados de um horário de funcionamento

        :param dia_semana: dia da semana (deve ser int 0-6)
        :param hora_inicio: hora de início no formato HH:MM
        :param hora_fim: hora de fim no formato HH:MM
        :raises ValidationException: se os dados não forem válidos
        """
        # Valida dia_semana
        if dia_semana is None:
            raise ValidationException("O dia da semana é obrigatório")

        try:
            dia_semana_int = int(dia_semana)
        except (ValueError, TypeError):
            raise ValidationException("O dia da semana deve ser um número inteiro")

        if not (0 <= dia_semana_int <= 6):
            raise ValidationException("O dia da semana deve ser um valor entre 0 (Segunda-feira) e 6 (Domingo)")

        # Valida hora_inicio
        if not hora_inicio or not str(hora_inicio).strip():
            raise ValidationException("A hora de início é obrigatória")

        # Valida hora_fim
        if not hora_fim or not str(hora_fim).strip():
            raise ValidationException("A hora de fim é obrigatória")

        _formato = "%H:%M"
        try:
            hora_inicio_dt = datetime.strptime(str(hora_inicio)[:5], _formato)
        except ValueError:
            raise ValidationException("A hora de início deve estar no formato HH:MM")

        try:
            hora_fim_dt = datetime.strptime(str(hora_fim)[:5], _formato)
        except ValueError:
            raise ValidationException("A hora de fim deve estar no formato HH:MM")

        # Valida que hora_fim é maior que hora_inicio
        if hora_fim_dt <= hora_inicio_dt:
            raise ValidationException("A hora de fim deve ser maior que a hora de início")

    def validar_conflito_horario(self, dia_semana: int, horarios_existentes: list) -> None:
        """
        Valida que não existe conflito de dia da semana com horários já cadastrados

        :param dia_semana: dia da semana a ser verificado (0-6)
        :param horarios_existentes: lista de objetos HorarioFuncionamento já cadastrados para o mesmo dia
        :raises ValidationException: se já existir um horário para o dia informado
        """
        if horarios_existentes:
            nome_dia = HorarioFuncionamento.DIAS_SEMANA.get(int(dia_semana), f"dia {dia_semana}")
            raise ValidationException(
                f"Já existe um horário de funcionamento cadastrado para {nome_dia}"
            )
