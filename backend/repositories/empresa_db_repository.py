from models.empresa import Empresa
from config.database import DBConnection
from exceptions import DatabaseException, NotFoundException
import pymysql


class EmpresaDBRepository:
    """Repositório para operações de persistência de Empresa em banco de dados"""

    def __init__(self):
        """
        Inicializa o repositório com a conexão ao banco de dados
        """
        self.db = DBConnection()

    def _get_connection(self):
        """Cria uma conexão com o banco de dados"""
        return self.db.get_connection()

    def buscar(self):
        """
        Busca o registro único da empresa

        :return: Objeto Empresa
        :raises NotFoundException: se a empresa não estiver cadastrada
        """
        connection = self._get_connection()
        try:
            with connection.cursor() as cursor:
                sql = """
                    SELECT id, nome, descricao, endereco, cnpj, telefone, email
                    FROM empresa
                    LIMIT 1
                """
                cursor.execute(sql)
                row = cursor.fetchone()

                if not row:
                    raise NotFoundException("Empresa não encontrada")

                return Empresa(
                    id=row['id'],
                    nome=row['nome'],
                    descricao=row['descricao'],
                    endereco=row['endereco'],
                    cnpj=row['cnpj'],
                    telefone=row['telefone'],
                    email=row['email']
                )
        except NotFoundException:
            raise
        except pymysql.Error as e:
            raise DatabaseException(f"Erro ao buscar empresa: {str(e)}")
        finally:
            connection.close()

    def atualizar(self, empresa):
        """
        Atualiza os dados da empresa

        :param empresa: Objeto Empresa com os dados atualizados
        :return: Objeto Empresa atualizado
        """
        connection = self._get_connection()
        try:
            with connection.cursor() as cursor:
                sql = """
                    UPDATE empresa
                    SET nome = %s, descricao = %s, endereco = %s,
                        cnpj = %s, telefone = %s, email = %s
                    WHERE id = %s
                """
                cursor.execute(sql, (
                    empresa.nome,
                    empresa.descricao,
                    empresa.endereco,
                    empresa.cnpj,
                    empresa.telefone,
                    empresa.email,
                    empresa.id
                ))
                connection.commit()

                if cursor.rowcount == 0:
                    raise NotFoundException("Empresa não encontrada")

                return empresa
        except NotFoundException:
            raise
        except pymysql.Error as e:
            raise DatabaseException(f"Erro ao atualizar empresa: {str(e)}")
        finally:
            connection.close()


# Instância singleton
empresa_db_repository = EmpresaDBRepository()
