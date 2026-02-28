from datetime import datetime
from exceptions import ValidationException


class ValidacaoAgendamentoService:
    """Service para validação de dados de agendamento"""
    
    def validar_dados_obrigatorios(self, inicio, fim, cliente_id, barbeiro_id):
        """
        Valida se todos os campos obrigatórios estão presentes
        
        :param inicio: Data/hora de início
        :param fim: Data/hora de fim
        :param cliente_id: ID do cliente
        :param barbeiro_id: ID do barbeiro
        :raises ValidationException: se algum campo obrigatório estiver faltando
        """
        if not inicio:
            raise ValidationException("Data/hora de início é obrigatória")
        
        if not fim:
            raise ValidationException("Data/hora de fim é obrigatória")
        
        if not cliente_id:
            raise ValidationException("Cliente é obrigatório")
        
        if not barbeiro_id:
            raise ValidationException("Barbeiro é obrigatório")
    
    def converter_e_validar_datetime(self, inicio, fim):
        """
        Converte strings para datetime e valida o formato
        
        :param inicio: Data/hora de início (string ou datetime)
        :param fim: Data/hora de fim (string ou datetime)
        :return: tuple (inicio, fim) como objetos datetime
        :raises ValidationException: se o formato for inválido
        """
        # Converte strings para datetime se necessário
        if isinstance(inicio, str):
            try:
                inicio = datetime.fromisoformat(inicio.replace('Z', '+00:00'))
            except ValueError:
                raise ValidationException("Formato de data/hora de início inválido")
        
        if isinstance(fim, str):
            try:
                fim = datetime.fromisoformat(fim.replace('Z', '+00:00'))
            except ValueError:
                raise ValidationException("Formato de data/hora de fim inválido")
        
        return inicio, fim
    
    def validar_ordem_horarios(self, inicio, fim):
        """
        Valida que a data/hora de fim é posterior à de início
        
        :param inicio: Data/hora de início (datetime)
        :param fim: Data/hora de fim (datetime)
        :raises ValidationException: se fim não for posterior a inicio
        """
        if fim <= inicio:
            raise ValidationException("Data/hora de fim deve ser posterior à data/hora de início")
    
    def validar_cliente_existe(self, cliente):
        """
        Valida que o cliente existe
        
        :param cliente: Objeto Cliente ou None
        :raises ValidationException: se cliente não existir
        """
        if not cliente:
            raise ValidationException("Cliente não encontrado")
    
    def validar_barbeiro_existe_e_eh_barbeiro(self, funcionario):
        """
        Valida que o funcionário existe e é um barbeiro
        
        :param funcionario: Objeto Funcionario ou None
        :raises ValidationException: se funcionário não existir ou não for barbeiro
        """
        if not funcionario:
            raise ValidationException("Funcionário não encontrado")
        
        if not funcionario.eh_barbeiro:
            raise ValidationException("Funcionário informado não é um barbeiro")
    
    def validar_conflito_horarios(self, barbeiro_id, inicio, fim, agendamentos_barbeiro, agendamento_id_atual=None):
        """
        Valida que o barbeiro não tem outro agendamento conflitante no horário
        
        :param barbeiro_id: ID do barbeiro
        :param inicio: Data/hora de início do agendamento (datetime)
        :param fim: Data/hora de fim do agendamento (datetime)
        :param agendamentos_barbeiro: Lista de objetos Agendamento do barbeiro
        :param agendamento_id_atual: ID do agendamento atual (para atualização, ignora conflito consigo mesmo)
        :raises ValidationException: se houver conflito de horários
        """
        for agendamento in agendamentos_barbeiro:
            # Se estamos atualizando, ignora o próprio agendamento
            if agendamento_id_atual and agendamento.id == agendamento_id_atual:
                continue
            
            # Converte para datetime se necessário
            agend_inicio = agendamento.inicio
            agend_fim = agendamento.fim
            
            if isinstance(agend_inicio, str):
                agend_inicio = datetime.fromisoformat(agend_inicio.replace('Z', '+00:00'))
            
            if isinstance(agend_fim, str):
                agend_fim = datetime.fromisoformat(agend_fim.replace('Z', '+00:00'))
            
            # Verifica se há sobreposição de horários
            # Há conflito se:
            # - O novo agendamento começa durante um agendamento existente
            # - O novo agendamento termina durante um agendamento existente
            # - O novo agendamento envolve completamente um agendamento existente
            if (inicio < agend_fim and fim > agend_inicio):
                raise ValidationException(
                    f"O barbeiro já possui um agendamento neste horário "
                    f"({agend_inicio.strftime('%d/%m/%Y %H:%M')} - {agend_fim.strftime('%d/%m/%Y %H:%M')})"
                )
