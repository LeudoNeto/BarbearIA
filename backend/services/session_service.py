import uuid
from datetime import datetime, timedelta
from typing import Optional
from exceptions import ValidationException


class SessionService:
    """Service para gerenciamento de sessões de usuários"""
    
    def __init__(self):
        """
        Inicializa o serviço de sessões
        Armazena sessões em memória (em produção, usar Redis ou similar)
        """
        self._sessions = {}  # session_id -> {'usuario': dict, 'expires_at': datetime}
        self._session_duration = timedelta(hours=24)  # Sessão válida por 24 horas
    
    def criar_sessao(self, usuario_dict: dict) -> str:
        """
        Cria uma nova sessão para o usuário
        
        :param usuario_dict: Dicionário com dados do usuário
        :return: ID da sessão criada
        """
        session_id = str(uuid.uuid4())
        expires_at = datetime.now() + self._session_duration
        
        self._sessions[session_id] = {
            'usuario': usuario_dict,
            'expires_at': expires_at
        }
        
        return session_id
    
    def obter_usuario_da_sessao(self, session_id: str) -> Optional[dict]:
        """
        Obtém os dados do usuário a partir do ID da sessão
        
        :param session_id: ID da sessão
        :return: Dicionário com dados do usuário ou None se sessão inválida/expirada
        """
        if not session_id or session_id not in self._sessions:
            raise ValidationException("Sessão inválida ou expirada")
        
        sessao = self._sessions[session_id]
        
        # Verifica se a sessão expirou
        if datetime.now() > sessao['expires_at']:
            del self._sessions[session_id]
            raise ValidationException("Sessão expirada")
        
        return sessao['usuario']
    
    def renovar_sessao(self, session_id: str) -> bool:
        """
        Renova o tempo de expiração de uma sessão
        
        :param session_id: ID da sessão
        :return: True se renovada com sucesso, False se sessão não existe
        """
        if session_id in self._sessions:
            self._sessions[session_id]['expires_at'] = datetime.now() + self._session_duration
            return True
        return False
    
    def destruir_sessao(self, session_id: str) -> bool:
        """
        Remove uma sessão (logout)
        
        :param session_id: ID da sessão
        :return: True se removida com sucesso, False se sessão não existe
        """
        if session_id in self._sessions:
            del self._sessions[session_id]
            return True
        return False
    
    def limpar_sessoes_expiradas(self):
        """
        Remove todas as sessões expiradas
        Útil para limpeza periódica
        """
        agora = datetime.now()
        sessoes_expiradas = [
            sid for sid, sessao in self._sessions.items()
            if agora > sessao['expires_at']
        ]
        
        for sid in sessoes_expiradas:
            del self._sessions[sid]


# Instância singleton
session_service = SessionService()
