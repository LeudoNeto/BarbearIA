from datetime import datetime


class AcessoUsuario:
    """Classe que representa um registro de acesso de usuario no sistema."""

    def __init__(self, id=None, usuario_id=None, tipo_usuario=None, email=None, data_hora_acesso=None):
        self.id = id
        self.usuario_id = usuario_id
        self.tipo_usuario = tipo_usuario
        self.email = email
        self.data_hora_acesso = data_hora_acesso

    def to_dict(self):
        """Converte o objeto para dicionario."""
        data_hora = self.data_hora_acesso
        if isinstance(data_hora, datetime):
            data_hora = data_hora.isoformat()

        return {
            'id': self.id,
            'usuario_id': self.usuario_id,
            'tipo_usuario': self.tipo_usuario,
            'email': self.email,
            'data_hora_acesso': data_hora
        }
