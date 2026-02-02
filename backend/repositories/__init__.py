from .cliente_db_repository import ClienteDBRepository
from .funcionario_db_repository import FuncionarioDBRepository
from .cliente_memory_repository import ClienteMemoryRepository
from .funcionario_memory_repository import FuncionarioMemoryRepository

__all__ = [
    'ClienteDBRepository',
    'FuncionarioDBRepository',
    'ClienteMemoryRepository',
    'FuncionarioMemoryRepository'
]
