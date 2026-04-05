from services.observer import Observer


class AgendamentoEmailObserver(Observer):
    """Observador que simula envio de e-mails para eventos de agendamento."""

    def update(self, event_type: str, data: any):
        """Simula o envio de e-mail."""
        if event_type == "agendamento_criado":
            cliente_id = data.get('cliente_id')
            inicio = data.get('inicio')
            print(f"[EMAIL][Observer] Enviando confirmação para Cliente ID {cliente_id}: "
                  f"Seu agendamento para {inicio} foi criado com sucesso!")
        elif event_type == "agendamento_deletado":
            print(f"[EMAIL][Observer] Enviando aviso para Cliente ID {data.get('cliente_id')}: "
                  f"Seu agendamento para {data.get('inicio')} foi apagado.")
        elif event_type == "agendamento_confirmado":
            print(f"[EMAIL][Observer] Enviando confirmação oficial para Cliente ID {data.get('cliente_id')}: "
                  f"O barbeiro aprovou seu agendamento para {data.get('inicio')}.")
        elif event_type == "agendamento_cancelado":
            print(f"[EMAIL][Observer] Enviando aviso de cancelamento para Cliente ID {data.get('cliente_id')}: "
                  f"Lamentamos, seu agendamento para {data.get('inicio')} foi cancelado.")
        elif event_type == "agendamento_concluido":
            print(f"[EMAIL][Observer] Enviando agradecimento para Cliente ID {data.get('cliente_id')}: "
                  f"Obrigado por comparecer ao serviço no horário {data.get('inicio')}! Volte sempre.")
