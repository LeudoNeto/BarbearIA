"""
Configuração de Persistência - Define o tipo de persistência usado no sistema
"""
import os


class PersistenceConfig:
    """Classe para gerenciar a configuração de persistência"""
    
    # Tipos de persistência disponíveis
    DATABASE = "database"
    MEMORY = "memory"
    
    def __init__(self):
        # Lê a variável de ambiente PERSISTENCE_TYPE
        # Valores aceitos: "database" ou "memory"
        # Padrão: "database"
        self.persistence_type = os.getenv("PERSISTENCE_TYPE", self.DATABASE).lower()
        
        # Valida o tipo de persistência
        if self.persistence_type not in [self.DATABASE, self.MEMORY]:
            raise ValueError(
                f"Tipo de persistência inválido: {self.persistence_type}. "
                f"Use 'database' ou 'memory'"
            )
    
    def is_database(self):
        """Verifica se está usando persistência em banco de dados"""
        return self.persistence_type == self.DATABASE
    
    def is_memory(self):
        """Verifica se está usando persistência em memória"""
        return self.persistence_type == self.MEMORY


# Instância singleton
persistence_config = PersistenceConfig()
