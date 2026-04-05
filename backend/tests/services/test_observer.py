import pytest
from unittest.mock import MagicMock
from services.observer import Observer, Observable
from services.observers.agendamento_logging_observer import AgendamentoLoggingObserver
from services.observers.agendamento_email_observer import AgendamentoEmailObserver


class TestObservable:
    """Testes para a classe base Observable."""

    def test_attach_observer(self):
        """Testa a adição de um observador ao Observable."""
        observable = Observable()
        observer = MagicMock(spec=Observer)
        
        observable.attach(observer)
        assert observer in observable._observers
        assert len(observable._observers) == 1
        
        # Tentar adicionar o mesmo observador novamente não deve duplicá-lo
        observable.attach(observer)
        assert len(observable._observers) == 1

    def test_detach_observer(self):
        """Testa a remoção de um observador do Observable."""
        observable = Observable()
        observer = MagicMock(spec=Observer)
        
        observable.attach(observer)
        observable.detach(observer)
        assert observer not in observable._observers
        assert len(observable._observers) == 0
        
        # Tentar remover um observador que não está na lista não deve gerar erro
        try:
            observable.detach(observer) 
        except Exception as e:
            pytest.fail(f"Detach com observador inexistente gerou erro: {e}")

    def test_notify_observers(self):
        """Testa se a notificação chama o método update de todos os observadores."""
        observable = Observable()
        observer1 = MagicMock(spec=Observer)
        observer2 = MagicMock(spec=Observer)
        
        observable.attach(observer1)
        observable.attach(observer2)
        
        data = {"id": 1, "cliente_id": 2}
        observable.notify("agendamento_criado", data)
        
        observer1.update.assert_called_once_with("agendamento_criado", data)
        observer2.update.assert_called_once_with("agendamento_criado", data)


class TestAgendamentoLoggingObserver:
    """Testes para o observador de log."""

    def test_update_agendamento_criado(self, capsys):
        """Testa o log de criação de agendamento."""
        observer = AgendamentoLoggingObserver()
        data = {"id": 10, "cliente_id": 5}
        observer.update("agendamento_criado", data)
        
        captured = capsys.readouterr()
        assert "[LOG][Observer] Novo agendamento criado: ID 10 - Cliente 5" in captured.out

    def test_update_agendamento_deletado(self, capsys):
        """Testa o log de remoção de agendamento."""
        observer = AgendamentoLoggingObserver()
        data = {"id": 10}
        observer.update("agendamento_deletado", data)
        
        captured = capsys.readouterr()
        assert "[LOG][Observer] Agendamento removido: ID 10" in captured.out

    def test_update_agendamento_atualizado(self, capsys):
        """Testa o log de atualização de agendamento."""
        observer = AgendamentoLoggingObserver()
        data = {"id": 10}
        observer.update("agendamento_atualizado", data)
        
        captured = capsys.readouterr()
        assert "[LOG][Observer] Agendamento atualizado: ID 10" in captured.out

    def test_update_outro_evento_ignorado(self, capsys):
        """Testa se o log ignora eventos não mapeados."""
        observer = AgendamentoLoggingObserver()
        data = {"id": 10}
        observer.update("evento_desconhecido", data)
        
        captured = capsys.readouterr()
        assert captured.out == ""


class TestAgendamentoEmailObserver:
    """Testes para o observador de e-mail."""

    def test_update_agendamento_criado(self, capsys):
        """Testa a simulação de e-mail na criação de agendamento."""
        observer = AgendamentoEmailObserver()
        data = {"cliente_id": 5, "inicio": "2023-10-10 10:00"}
        observer.update("agendamento_criado", data)
        
        captured = capsys.readouterr()
        assert "[EMAIL][Observer] Enviando confirmação para Cliente ID 5:" in captured.out
        assert "Seu agendamento para 2023-10-10 10:00 foi criado com sucesso!" in captured.out

    def test_update_agendamento_deletado(self, capsys):
        """Testa a simulação de e-mail no cancelamento de agendamento."""
        observer = AgendamentoEmailObserver()
        # O código original busca inicio também na deleção: "...para {data.get('inicio')} foi cancelado."
        data = {"cliente_id": 5, "inicio": "2023-10-10 10:00"}
        observer.update("agendamento_deletado", data)
        
        captured = capsys.readouterr()
        assert "[EMAIL][Observer] Enviando aviso para Cliente ID 5:" in captured.out
        assert "Seu agendamento para 2023-10-10 10:00 foi cancelado." in captured.out

    def test_update_outro_evento_ignorado(self, capsys):
        """Testa se a simulação de e-mail ignora eventos não mapeados."""
        observer = AgendamentoEmailObserver()
        data = {"id": 10}
        observer.update("evento_desconhecido", data)
        
        captured = capsys.readouterr()
        assert captured.out == ""
