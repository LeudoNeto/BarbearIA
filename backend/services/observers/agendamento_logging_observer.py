from services.observer import Observer


class AgendamentoLoggingObserver(Observer):
    """Observador que registra eventos de agendamento no console."""

    def update(self, event_type: str, data: any):
        """Implementação do update para log."""
        if event_type == "agendamento_criado":
            print(f"[LOG][Observer] Novo agendamento criado: ID {data.get('id')} - Cliente {data.get('cliente_id')}")
        elif event_type == "agendamento_deletado":
            print(f"[LOG][Observer] Agendamento removido: ID {data.get('id')}")
        elif event_type == "agendamento_atualizado":
            print(f"[LOG][Observer] Agendamento atualizado: ID {data.get('id')}")
        elif event_type == "agendamento_confirmado":
            print(f"[LOG][Observer] Agendamento confirmado: ID {data.get('id')}")
        elif event_type == "agendamento_cancelado":
            print(f"[LOG][Observer] Agendamento cancelado: ID {data.get('id')}")
        elif event_type == "agendamento_concluido":
            print(f"[LOG][Observer] Agendamento concluído: ID {data.get('id')}")
