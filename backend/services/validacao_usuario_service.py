import re
from exceptions import ValidationException


class ValidacaoUsuarioService:
    """Service para validação de dados de usuário"""
    
    def validar_email(self, email: str) -> None:
        """
        Valida o email do usuário
        
        :param email: email a ser validado
        :raises ValidationException: se o email não atender aos requisitos
        """
        # Verifica se o email não é vazio
        if not email or not email.strip():
            raise ValidationException("O email não pode ser vazio")
        
        # Verifica o tamanho máximo (255 caracteres)
        if len(email) > 255:
            raise ValidationException("O email não pode ter mais de 255 caracteres")
                
        # Verifica o formato básico do email
        email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(email_regex, email):
            raise ValidationException("O email fornecido não é válido")
    
    def validar_senha(self, senha: str, email: str = None, nome: str = None) -> None:
        """
        Valida a senha do usuário
        
        :param senha: senha a ser validada
        :param email: email do usuário (opcional, para verificar se não é idêntico)
        :param nome: nome do usuário (opcional, para verificar se não é idêntico)
        :raises ValidationException: se a senha não atender aos requisitos
        """
        # Verifica se a senha não é vazia
        if not senha:
            raise ValidationException("A senha não pode ser vazia")
        
        # Verifica o tamanho mínimo (8) e máximo (128)
        if len(senha) < 8:
            raise ValidationException("A senha deve ter no mínimo 8 caracteres")
        
        if len(senha) > 128:
            raise ValidationException("A senha deve ter no máximo 128 caracteres")
        
        # Conta quantos tipos de caracteres estão presentes
        tipos_presentes = 0
        
        # Verifica maiúsculas
        if re.search(r'[A-Z]', senha):
            tipos_presentes += 1
        
        # Verifica minúsculas
        if re.search(r'[a-z]', senha):
            tipos_presentes += 1
        
        # Verifica números
        if re.search(r'\d', senha):
            tipos_presentes += 1
        
        # Verifica caracteres não alfanuméricos
        if re.search(r'[!@#$%^&*()\-_+=\[\]{}|\'"]', senha):
            tipos_presentes += 1
        
        # Requer no mínimo 3 tipos
        if tipos_presentes < 3:
            raise ValidationException(
                "A senha deve conter no mínimo 3 dos seguintes tipos de caracteres: "
                "maiúsculas, minúsculas, números e caracteres especiais (! @ # $ % ^ & * ( ) _ + - = [ ] { } | ')"
            )
        
        # Verifica se a senha não é idêntica ao nome (se fornecido)
        if nome and senha.lower() == nome.lower():
            raise ValidationException("A senha não pode ser idêntica ao nome")
        
        # Verifica se a senha não é idêntica ao email (se fornecido)
        if email and senha.lower() == email.lower():
            raise ValidationException("A senha não pode ser idêntica ao endereço de e-mail")
