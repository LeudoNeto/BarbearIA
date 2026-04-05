from models.empresa import Empresa
from exceptions import ValidationException
from managers.memento import EmpresaCaretaker, EmpresaOriginator
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
        self._originator = EmpresaOriginator()
        self._caretaker = EmpresaCaretaker()

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
        empresa_atual = self.empresa_repository.buscar()
        snapshot_anterior = self._originator.salvar_estado(empresa_atual)

        empresa_atualizada = Empresa(
            id=empresa_atual.id,
            nome=dados.get('nome', empresa_atual.nome),
            descricao=dados.get('descricao', empresa_atual.descricao),
            endereco=dados.get('endereco', empresa_atual.endereco),
            cnpj=dados.get('cnpj', empresa_atual.cnpj),
            telefone=dados.get('telefone', empresa_atual.telefone),
            email=dados.get('email', empresa_atual.email)
        )

        # Valida o email se foi fornecido ou já existia
        if empresa_atualizada.email:
            self.validacao_service.validar_email(empresa_atualizada.email)

        self.empresa_repository.atualizar(empresa_atualizada)
        self._caretaker.salvar(snapshot_anterior)

        return empresa_atualizada.to_dict()

    def desfazer_ultima_atualizacao(self):
        """
        Desfaz a última atualização realizada nos dados da empresa.

        :return: dict com o estado restaurado da empresa
        """
        ultimo_estado = self._caretaker.recuperar()
        if not ultimo_estado:
            raise ValidationException("Não há atualização de empresa para desfazer")

        empresa_restaurada = self._originator.restaurar_estado(ultimo_estado)
        self.empresa_repository.atualizar(empresa_restaurada)

        return empresa_restaurada.to_dict()


# Instância singleton
empresa_manager = EmpresaManager()
