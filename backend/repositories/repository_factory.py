"""
Factory para criar repositórios baseado na configuração de persistência
"""
from config.persistence import persistence_config


class RepositoryFactory:
    """Factory para criar instâncias de repositórios"""
    
    @staticmethod
    def get_cliente_repository():
        """
        Retorna o repositório de cliente apropriado baseado na configuração
        
        :return: Instância do repositório de cliente
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
        Retorna o repositório de funcionário apropriado baseado na configuração
        
        :return: Instância do repositório de funcionário
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
        Retorna o repositório de empresa apropriado baseado na configuração

        :return: Instância do repositório de empresa
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
        Retorna o repositório de horário de funcionamento apropriado baseado na configuração

        :return: Instância do repositório de horário de funcionamento
        """
        if persistence_config.is_memory():
            from repositories.horario_funcionamento_memory_repository import horario_funcionamento_memory_repository
            return horario_funcionamento_memory_repository
        else:
            from repositories.horario_funcionamento_db_repository import horario_funcionamento_db_repository
            return horario_funcionamento_db_repository


# Instância singleton
repository_factory = RepositoryFactory()
