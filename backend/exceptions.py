from fastapi import HTTPException, status
import logging

# Configurar logging para erros do sistema
logging.basicConfig(
    level=logging.ERROR,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('error.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


class ValidationException(HTTPException):
    """Exceção para erros de validação"""
    def __init__(self, message: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message
        )


class DatabaseException(HTTPException):
    """Exceção para erros de banco de dados"""
    def __init__(self, message: str):
        logger.error(f"DatabaseException: {message}", exc_info=True)
        
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor. Por favor, tente novamente mais tarde."
        )


class DatabaseConnectionException(HTTPException):
    """Exceção para erros de conexão com o banco de dados"""
    def __init__(self, message: str = "Não foi possível conectar ao banco de dados"):
        logger.error(f"DatabaseConnectionException: {message}", exc_info=True)
        
        super().__init__(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Serviço temporariamente indisponível. Por favor, tente novamente em alguns instantes."
        )


class DuplicateException(HTTPException):
    """Exceção para erros de duplicação (ex: email já existe)"""
    def __init__(self, message: str):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=message
        )


class NotFoundException(HTTPException):
    """Exceção para recursos não encontrados"""
    def __init__(self, message: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=message
        )


class UnauthorizedException(HTTPException):
    """Exceção para erros de autenticação"""
    def __init__(self, message: str = "Não autorizado"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=message
        )


class ForbiddenException(HTTPException):
    """Exceção para erros de permissão"""
    def __init__(self, message: str = "Acesso negado"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=message
        )


class StateTransitionException(HTTPException):
    """Exceção para transições de estado inválidas"""
    def __init__(self, message: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message
        )

