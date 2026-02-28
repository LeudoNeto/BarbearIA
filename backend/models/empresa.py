class Empresa:
    """Classe que representa a empresa (barbearia) no sistema"""

    def __init__(self, id=None, nome=None, descricao=None, endereco=None,
                 cnpj=None, telefone=None, email=None):
        self.id = id
        self.nome = nome
        self.descricao = descricao
        self.endereco = endereco
        self.cnpj = cnpj
        self.telefone = telefone
        self.email = email

    def to_dict(self):
        """Converte o objeto para dicionário"""
        return {
            'id': self.id,
            'nome': self.nome,
            'descricao': self.descricao,
            'endereco': self.endereco,
            'cnpj': self.cnpj,
            'telefone': self.telefone,
            'email': self.email
        }
