"""
Factory para criar repositorios baseado na configuracao de persistencia
"""
from config.persistence import persistence_config


class RepositoryFactory:
    """Factory para criar instancias de repositorios"""

    @staticmethod
    def get_cliente_repository():
        """
        Retorna o repositorio de cliente apropriado baseado na configuracao.

        :return: Instancia do repositorio de cliente
        """
        if persistence_config.is_memory():
            from repositories.cliente_memory_repository import cliente_memory_repository
            return cliente_memory_repository
        else:
            from repositories.cliente_db_repository import cliente_db_repository
            return cliente_db_repository

    @staticmethod
    def get_funcionario_repository():
        """
        Retorna o repositorio de funcionario apropriado baseado na configuracao.

        :return: Instancia do repositorio de funcionario
        """
        if persistence_config.is_memory():
            from repositories.funcionario_memory_repository import funcionario_memory_repository
            return funcionario_memory_repository
        else:
            from repositories.funcionario_db_repository import funcionario_db_repository
            return funcionario_db_repository

    @staticmethod
    def get_empresa_repository():
        """
        Retorna o repositorio de empresa apropriado baseado na configuracao.

        :return: Instancia do repositorio de empresa
        """
        if persistence_config.is_memory():
            from repositories.empresa_memory_repository import empresa_memory_repository
            return empresa_memory_repository
        else:
            from repositories.empresa_db_repository import empresa_db_repository
            return empresa_db_repository

    @staticmethod
    def get_horario_funcionamento_repository():
        """
        Retorna o repositorio de horario de funcionamento apropriado baseado na configuracao.

        :return: Instancia do repositorio de horario de funcionamento
        """
        if persistence_config.is_memory():
            from repositories.horario_funcionamento_memory_repository import horario_funcionamento_memory_repository
            return horario_funcionamento_memory_repository
        else:
            from repositories.horario_funcionamento_db_repository import horario_funcionamento_db_repository
            return horario_funcionamento_db_repository

    @staticmethod
    def get_agendamento_repository():
        """
        Retorna o repositorio de agendamento apropriado baseado na configuracao.

        :return: Instancia do repositorio de agendamento
        """
        if persistence_config.is_memory():
            from repositories.agendamento_memory_repository import agendamento_memory_repository
            return agendamento_memory_repository
        else:
            from repositories.agendamento_db_repository import agendamento_db_repository
            return agendamento_db_repository

    @staticmethod
    def get_acesso_usuario_repository():
        """
        Retorna o repositorio de historico de acessos apropriado baseado na configuracao.

        :return: Instancia do repositorio de acesso de usuario
        """
        if persistence_config.is_memory():
            from repositories.acesso_usuario_memory_repository import acesso_usuario_memory_repository
            return acesso_usuario_memory_repository
        else:
            from repositories.acesso_usuario_db_repository import acesso_usuario_db_repository
            return acesso_usuario_db_repository


repository_factory = RepositoryFactory()
