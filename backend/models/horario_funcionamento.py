class HorarioFuncionamento:
    """Classe que representa um horário de funcionamento da empresa"""

    DIAS_SEMANA = {
        0: 'Segunda-feira',
        1: 'Terça-feira',
        2: 'Quarta-feira',
        3: 'Quinta-feira',
        4: 'Sexta-feira',
        5: 'Sábado',
        6: 'Domingo'
    }

    def __init__(self, id=None, dia_semana=None, hora_inicio=None, hora_fim=None):
        self.id = id
        self.dia_semana = dia_semana  # 0 = Segunda-feira, 6 = Domingo
        self.hora_inicio = hora_inicio  # formato HH:MM
        self.hora_fim = hora_fim        # formato HH:MM

    def to_dict(self):
        """Converte o objeto para dicionário"""
        return {
            'id': self.id,
            'dia_semana': self.dia_semana,
            'dia_semana_nome': self.DIAS_SEMANA.get(self.dia_semana),
            'hora_inicio': str(self.hora_inicio) if self.hora_inicio else None,
            'hora_fim': str(self.hora_fim) if self.hora_fim else None
        }
