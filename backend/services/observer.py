from abc import ABC, abstractmethod


class Observer(ABC):
    """Interface abstrata para observadores."""

    @abstractmethod
    def update(self, event_type: str, data: any):
        """Método chamado quando o sujeito notifica mudança."""
        pass


class Observable:
    """Classe base para objetos que desejam ser observados."""

    def __init__(self):
        self._observers = []

    def attach(self, observer: Observer):
        """Adiciona um observador."""
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: Observer):
        """Remove um observador."""
        try:
            self._observers.remove(observer)
        except ValueError:
            pass

    def notify(self, event_type: str, data: any):
        """Notifica todos os observadores sobre um evento."""
        for observer in self._observers:
            observer.update(event_type, data)
