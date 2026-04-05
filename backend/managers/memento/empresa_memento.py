from dataclasses import dataclass

from models.empresa import Empresa


@dataclass(frozen=True)
class EmpresaMemento:
    """Snapshot imutavel do estado da empresa para suporte a undo."""

    estado: dict


class EmpresaOriginator:
    """Responsavel por criar e restaurar snapshots da empresa."""

    def salvar_estado(self, empresa: Empresa) -> EmpresaMemento:
        return EmpresaMemento(estado=empresa.to_dict().copy())

    def restaurar_estado(self, memento: EmpresaMemento) -> Empresa:
        return Empresa(**memento.estado)


class EmpresaCaretaker:
    """Armazena apenas o ultimo snapshot para undo de uma operacao."""

    def __init__(self):
        self._ultimo_memento = None

    def salvar(self, memento: EmpresaMemento):
        self._ultimo_memento = memento

    def recuperar(self):
        memento = self._ultimo_memento
        self._ultimo_memento = None
        return memento
