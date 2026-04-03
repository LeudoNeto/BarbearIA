from models.acesso_usuario import AcessoUsuario


class AcessoUsuarioMemoryRepository:
    """Repositorio em memoria para historico de acessos de usuario."""

    def __init__(self):
        self._acessos = {}
        self._next_id = 1

    def criar(self, acesso_usuario):
        """
        Cria um novo registro de acesso em memoria.

        :param acesso_usuario: Objeto AcessoUsuario
        :return: ID do acesso criado
        """
        if not isinstance(acesso_usuario, AcessoUsuario):
            raise TypeError("acesso_usuario deve ser uma instancia de AcessoUsuario")

        acesso_usuario.id = self._next_id
        self._acessos[self._next_id] = acesso_usuario
        self._next_id += 1
        return acesso_usuario.id

    def listar(self):
        """
        Lista todos os acessos registrados em memoria.

        :return: Lista de objetos AcessoUsuario
        """
        return sorted(
            self._acessos.values(),
            key=lambda acesso: (acesso.data_hora_acesso, acesso.id),
            reverse=True
        )

    def contar(self):
        """
        Conta o numero total de acessos registrados em memoria.

        :return: int com a quantidade de acessos
        """
        return len(self._acessos)


acesso_usuario_memory_repository = AcessoUsuarioMemoryRepository()
