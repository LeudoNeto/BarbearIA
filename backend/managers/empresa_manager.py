from services.validacao_usuario_service import ValidacaoUsuarioService
from repositories.repository_factory import repository_factory


class EmpresaManager:
    """Manager para orquestrar operações de Empresa"""

    def __init__(self):
        """
        Inicializa o manager
        """
        self.empresa_repository = repository_factory.get_empresa_repository()
        self.validacao_service = ValidacaoUsuarioService()

    def buscar_empresa(self):
        """
        Busca os dados da empresa

        :return: dict com dados da empresa
        """
        empresa = self.empresa_repository.buscar()
        return empresa.to_dict()

    def atualizar_empresa(self, dados):
        """
        Atualiza os dados da empresa

        :param dados: dict com os campos a atualizar (parcial ou total)
        :return: dict com os dados atualizados da empresa
        """
        empresa = self.empresa_repository.buscar()

        # Aplica os campos fornecidos (atualização parcial)
        empresa.nome = dados.get('nome', empresa.nome)
        empresa.descricao = dados.get('descricao', empresa.descricao)
        empresa.endereco = dados.get('endereco', empresa.endereco)
        empresa.cnpj = dados.get('cnpj', empresa.cnpj)
        empresa.telefone = dados.get('telefone', empresa.telefone)
        empresa.email = dados.get('email', empresa.email)

        # Valida o email se foi fornecido ou já existia
        if empresa.email:
            self.validacao_service.validar_email(empresa.email)

        self.empresa_repository.atualizar(empresa)
        return empresa.to_dict()


# Instância singleton
empresa_manager = EmpresaManager()
