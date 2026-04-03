import pymysql

from config.database import DBConnection
from exceptions import DatabaseException
from models.acesso_usuario import AcessoUsuario


class AcessoUsuarioDBRepository:
    """Repositorio para persistencia de historico de acessos em banco de dados."""

    def __init__(self):
        self.db = DBConnection()

    def _get_connection(self):
        return self.db.get_connection()

    def criar(self, acesso_usuario):
        """
        Cria um novo registro de acesso no banco de dados.

        :param acesso_usuario: Objeto AcessoUsuario
        :return: ID do acesso criado
        """
        connection = self._get_connection()
        try:
            with connection.cursor() as cursor:
                sql = """
                    INSERT INTO acessos_usuario (usuario_id, tipo_usuario, email, data_hora_acesso)
                    VALUES (%s, %s, %s, %s)
                """
                cursor.execute(sql, (
                    acesso_usuario.usuario_id,
                    acesso_usuario.tipo_usuario,
                    acesso_usuario.email,
                    acesso_usuario.data_hora_acesso
                ))
                connection.commit()
                return cursor.lastrowid
        except pymysql.Error as e:
            raise DatabaseException(f"Erro ao registrar acesso de usuario: {str(e)}")
        finally:
            connection.close()

    def listar(self):
        """
        Lista todos os acessos registrados.

        :return: Lista de objetos AcessoUsuario
        """
        connection = self._get_connection()
        try:
            with connection.cursor() as cursor:
                sql = """
                    SELECT id, usuario_id, tipo_usuario, email, data_hora_acesso
                    FROM acessos_usuario
                    ORDER BY data_hora_acesso DESC, id DESC
                """
                cursor.execute(sql)
                results = cursor.fetchall()

                acessos = []
                for row in results:
                    acessos.append(AcessoUsuario(
                        id=row['id'],
                        usuario_id=row['usuario_id'],
                        tipo_usuario=row['tipo_usuario'],
                        email=row['email'],
                        data_hora_acesso=row['data_hora_acesso']
                    ))

                return acessos
        except pymysql.Error as e:
            raise DatabaseException(f"Erro ao listar acessos de usuario: {str(e)}")
        finally:
            connection.close()

    def contar(self):
        """
        Conta o numero total de acessos registrados.

        :return: int com a quantidade de acessos
        """
        connection = self._get_connection()
        try:
            with connection.cursor() as cursor:
                sql = "SELECT COUNT(*) as total FROM acessos_usuario"
                cursor.execute(sql)
                row = cursor.fetchone()
                return row['total']
        except pymysql.Error as e:
            raise DatabaseException(f"Erro ao contar acessos de usuario: {str(e)}")
        finally:
            connection.close()


acesso_usuario_db_repository = AcessoUsuarioDBRepository()
