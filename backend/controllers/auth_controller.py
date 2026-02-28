from fastapi import APIRouter, Response, Cookie
from typing import Optional
from controllers.facade_controller import facade_controller


class AuthController:
    """Controller para rotas de autenticação"""
    
    def __init__(self):
        """
        Inicializa o controller
        """
        self.facade = facade_controller
        self.router = APIRouter(prefix='/auth', tags=['Autenticação'])
        self._registrar_rotas()
    
    def _registrar_rotas(self):
        """Registra as rotas do controller"""
        
        @self.router.post('/login')
        async def login(dados: dict, response: Response):
            """
            Realiza login de usuário (cliente ou funcionário)
            
            Espera um JSON com:
            - email: string
            - senha: string
            
            Retorna os dados do usuário com o campo 'tipo' indicando se é 'cliente' ou 'funcionario'
            Define um cookie de sessão para autenticação
            """
            usuario_dict, session_id = self.facade.login(dados)
            
            # Define cookie de sessão (HttpOnly para segurança)
            response.set_cookie(
                key="session_id",
                value=session_id,
                httponly=True,
                max_age=86400,  # 24 horas em segundos
                samesite="lax"
            )
            
            return usuario_dict
        
        @self.router.get('/me')
        async def obter_usuario_logado(session_id: Optional[str] = Cookie(None)):
            """
            Retorna os dados do usuário atualmente logado
            
            Requer cookie de sessão válido
            """
            return self.facade.obter_usuario_logado(session_id)
        
        @self.router.post('/logout')
        async def logout(response: Response, session_id: Optional[str] = Cookie(None)):
            """
            Realiza logout do usuário
            
            Remove a sessão e o cookie
            """
            if session_id:
                self.facade.logout(session_id)
            
            # Remove o cookie
            response.delete_cookie(key="session_id")
            
            return {"message": "Logout realizado com sucesso"}
        
        @self.router.post('/signup', status_code=201)
        async def signup(dados: dict):
            """
            Registra um novo cliente no sistema
            
            Espera um JSON com:
            - email: string (obrigatório)
            - senha: string (obrigatório)
            - telefone: string (obrigatório)
            - foto: string (opcional)
            """
            return self.facade.signup(dados)


# Instância singleton
auth_controller = AuthController()
