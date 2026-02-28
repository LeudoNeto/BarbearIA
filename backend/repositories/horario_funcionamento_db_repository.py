from models.horario_funcionamento import HorarioFuncionamento
from config.database import DBConnection
from exceptions import DatabaseException, NotFoundException, DuplicateException
import pymysql


class HorarioFuncionamentoDBRepository:
    """Repositório para operações de persistência de HorarioFuncionamento em banco de dados"""

    def __init__(self):
        """
        Inicializa o repositório com a conexão ao banco de dados
        """
        self.db = DBConnection()

    def _get_connection(self):
        """Cria uma conexão com o banco de dados"""
        return self.db.get_connection()

    def _row_to_obj(self, row):
        """Converte uma linha do banco em objeto HorarioFuncionamento"""
        return HorarioFuncionamento(
            id=row['id'],
            dia_semana=row['dia_semana'],
            hora_inicio=str(row['hora_inicio']),
            hora_fim=str(row['hora_fim'])
        )

    def listar(self):
        """
        Lista todos os horários de funcionamento ordenados por dia da semana

        :return: Lista de objetos HorarioFuncionamento
        """
        connection = self._get_connection()
        try:
            with connection.cursor() as cursor:
                sql = """
                    SELECT id, dia_semana, hora_inicio, hora_fim
                    FROM horarios_funcionamento
                    ORDER BY dia_semana
                """
                cursor.execute(sql)
                results = cursor.fetchall()
                return [self._row_to_obj(row) for row in results]
        except pymysql.Error as e:
            raise DatabaseException(f"Erro ao listar horários de funcionamento: {str(e)}")
        finally:
            connection.close()

    def buscar_por_id(self, id):
        """
        Busca um horário de funcionamento pelo ID

        :param id: ID do horário
        :return: Objeto HorarioFuncionamento
        :raises NotFoundException: se o horário não for encontrado
        """
        connection = self._get_connection()
        try:
            with connection.cursor() as cursor:
                sql = """
                    SELECT id, dia_semana, hora_inicio, hora_fim
                    FROM horarios_funcionamento
                    WHERE id = %s
                """
                cursor.execute(sql, (id,))
                row = cursor.fetchone()
                
                if row is None:
                    raise NotFoundException("Horário de funcionamento não encontrado")
                
                return self._row_to_obj(row)
        except NotFoundException:
            raise
        except pymysql.Error as e:
            raise DatabaseException(f"Erro ao buscar horário por ID: {str(e)}")
        finally:
            connection.close()

    def listar_por_dia(self, dia_semana, id_excluir=None):
        """
        Lista horários de um dia específico, opcionalmente excluindo um registro pelo ID

        :param dia_semana: dia da semana (0-6)
        :param id_excluir: ID a ser ignorado na busca (para validação de atualização)
        :return: Lista de objetos HorarioFuncionamento
        """
        connection = self._get_connection()
        try:
            with connection.cursor() as cursor:
                if id_excluir is not None:
                    sql = """
                        SELECT id, dia_semana, hora_inicio, hora_fim
                        FROM horarios_funcionamento
                        WHERE dia_semana = %s AND id != %s
                    """
                    cursor.execute(sql, (dia_semana, id_excluir))
                else:
                    sql = """
                        SELECT id, dia_semana, hora_inicio, hora_fim
                        FROM horarios_funcionamento
                        WHERE dia_semana = %s
                    """
                    cursor.execute(sql, (dia_semana,))
                results = cursor.fetchall()
                return [self._row_to_obj(row) for row in results]
        except pymysql.Error as e:
            raise DatabaseException(f"Erro ao buscar horários por dia: {str(e)}")
        finally:
            connection.close()

    def criar(self, horario):
        """
        Cria um novo horário de funcionamento

        :param horario: Objeto HorarioFuncionamento
        :return: ID do horário criado
        """
        connection = self._get_connection()
        try:
            with connection.cursor() as cursor:
                sql = """
                    INSERT INTO horarios_funcionamento (dia_semana, hora_inicio, hora_fim)
                    VALUES (%s, %s, %s)
                """
                cursor.execute(sql, (
                    horario.dia_semana,
                    horario.hora_inicio,
                    horario.hora_fim
                ))
                connection.commit()
                return cursor.lastrowid
        except pymysql.IntegrityError as e:
            if 'duplicate' in str(e).lower():
                raise DuplicateException("Já existe um horário cadastrado para este dia da semana")
            raise DatabaseException(f"Erro de integridade: {str(e)}")
        except pymysql.Error as e:
            raise DatabaseException(f"Erro ao criar horário de funcionamento: {str(e)}")
        finally:
            connection.close()

    def atualizar(self, horario):
        """
        Atualiza um horário de funcionamento existente

        :param horario: Objeto HorarioFuncionamento com os dados atualizados
        :return: Objeto HorarioFuncionamento atualizado
        :raises NotFoundException: se o horário não for encontrado
        """
        connection = self._get_connection()
        try:
            with connection.cursor() as cursor:
                sql = """
                    UPDATE horarios_funcionamento
                    SET dia_semana = %s, hora_inicio = %s, hora_fim = %s
                    WHERE id = %s
                """
                cursor.execute(sql, (
                    horario.dia_semana,
                    horario.hora_inicio,
                    horario.hora_fim,
                    horario.id
                ))
                connection.commit()

                if cursor.rowcount == 0:
                    raise NotFoundException("Horário de funcionamento não encontrado")

                return horario
        except NotFoundException:
            raise
        except pymysql.IntegrityError as e:
            if 'duplicate' in str(e).lower():
                raise DuplicateException("Já existe um horário cadastrado para este dia da semana")
            raise DatabaseException(f"Erro de integridade: {str(e)}")
        except pymysql.Error as e:
            raise DatabaseException(f"Erro ao atualizar horário de funcionamento: {str(e)}")
        finally:
            connection.close()

    def deletar(self, id):
        """
        Remove um horário de funcionamento pelo ID

        :param id: ID do horário a ser removido
        :raises NotFoundException: se o horário não for encontrado
        """
        connection = self._get_connection()
        try:
            with connection.cursor() as cursor:
                sql = "DELETE FROM horarios_funcionamento WHERE id = %s"
                cursor.execute(sql, (id,))
                connection.commit()

                if cursor.rowcount == 0:
                    raise NotFoundException("Horário de funcionamento não encontrado")
        except NotFoundException:
            raise
        except pymysql.Error as e:
            raise DatabaseException(f"Erro ao deletar horário de funcionamento: {str(e)}")
        finally:
            connection.close()


# Instância singleton
horario_funcionamento_db_repository = HorarioFuncionamentoDBRepository()
