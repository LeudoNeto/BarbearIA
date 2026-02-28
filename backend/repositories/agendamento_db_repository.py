from models.agendamento import Agendamento
from config.database import DBConnection
from exceptions import DatabaseException, NotFoundException
import pymysql
from datetime import datetime


class AgendamentoDBRepository:
    """Repositório para operações de persistência de Agendamento em banco de dados"""
    
    def __init__(self):
        """
        Inicializa o repositório com a conexão ao banco de dados
        """
        self.db = DBConnection()
    
    def _get_connection(self):
        """Cria uma conexão com o banco de dados"""
        return self.db.get_connection()
    
    def listar(self):
        """
        Lista todos os agendamentos
        
        :return: Lista de objetos Agendamento
        """
        connection = self._get_connection()
        try:
            with connection.cursor() as cursor:
                sql = """
                    SELECT id, inicio, fim, cliente_id, barbeiro_id 
                    FROM agendamentos
                """
                cursor.execute(sql)
                results = cursor.fetchall()
                
                agendamentos = []
                for row in results:
                    agendamento = Agendamento(
                        id=row['id'],
                        inicio=row['inicio'],
                        fim=row['fim'],
                        cliente_id=row['cliente_id'],
                        barbeiro_id=row['barbeiro_id']
                    )
                    agendamentos.append(agendamento)
                
                return agendamentos
        except pymysql.Error as e:
            raise DatabaseException(f"Erro ao listar agendamentos: {str(e)}")
        finally:
            connection.close()
    
    def buscar_por_id(self, agendamento_id):
        """
        Busca um agendamento pelo ID
        
        :param agendamento_id: ID do agendamento
        :return: Objeto Agendamento ou None se não encontrado
        """
        connection = self._get_connection()
        try:
            with connection.cursor() as cursor:
                sql = """
                    SELECT id, inicio, fim, cliente_id, barbeiro_id 
                    FROM agendamentos
                    WHERE id = %s
                """
                cursor.execute(sql, (agendamento_id,))
                row = cursor.fetchone()
                
                if row is None:
                    return None
                
                return Agendamento(
                    id=row['id'],
                    inicio=row['inicio'],
                    fim=row['fim'],
                    cliente_id=row['cliente_id'],
                    barbeiro_id=row['barbeiro_id']
                )
        except pymysql.Error as e:
            raise DatabaseException(f"Erro ao buscar agendamento por ID: {str(e)}")
        finally:
            connection.close()
    
    def buscar_por_cliente(self, cliente_id):
        """
        Busca todos os agendamentos de um cliente
        
        :param cliente_id: ID do cliente
        :return: Lista de objetos Agendamento
        """
        connection = self._get_connection()
        try:
            with connection.cursor() as cursor:
                sql = """
                    SELECT id, inicio, fim, cliente_id, barbeiro_id 
                    FROM agendamentos
                    WHERE cliente_id = %s
                """
                cursor.execute(sql, (cliente_id,))
                results = cursor.fetchall()
                
                agendamentos = []
                for row in results:
                    agendamento = Agendamento(
                        id=row['id'],
                        inicio=row['inicio'],
                        fim=row['fim'],
                        cliente_id=row['cliente_id'],
                        barbeiro_id=row['barbeiro_id']
                    )
                    agendamentos.append(agendamento)
                
                return agendamentos
        except pymysql.Error as e:
            raise DatabaseException(f"Erro ao buscar agendamentos por cliente: {str(e)}")
        finally:
            connection.close()
    
    def buscar_por_barbeiro(self, barbeiro_id):
        """
        Busca todos os agendamentos de um barbeiro
        
        :param barbeiro_id: ID do barbeiro
        :return: Lista de objetos Agendamento
        """
        connection = self._get_connection()
        try:
            with connection.cursor() as cursor:
                sql = """
                    SELECT id, inicio, fim, cliente_id, barbeiro_id 
                    FROM agendamentos
                    WHERE barbeiro_id = %s
                """
                cursor.execute(sql, (barbeiro_id,))
                results = cursor.fetchall()
                
                agendamentos = []
                for row in results:
                    agendamento = Agendamento(
                        id=row['id'],
                        inicio=row['inicio'],
                        fim=row['fim'],
                        cliente_id=row['cliente_id'],
                        barbeiro_id=row['barbeiro_id']
                    )
                    agendamentos.append(agendamento)
                
                return agendamentos
        except pymysql.Error as e:
            raise DatabaseException(f"Erro ao buscar agendamentos por barbeiro: {str(e)}")
        finally:
            connection.close()
    
    def criar(self, agendamento):
        """
        Cria um novo agendamento no banco de dados
        
        :param agendamento: Objeto Agendamento
        :return: ID do agendamento criado
        """
        connection = self._get_connection()
        try:
            with connection.cursor() as cursor:
                sql = """
                    INSERT INTO agendamentos (inicio, fim, cliente_id, barbeiro_id)
                    VALUES (%s, %s, %s, %s)
                """
                cursor.execute(sql, (
                    agendamento.inicio,
                    agendamento.fim,
                    agendamento.cliente_id,
                    agendamento.barbeiro_id
                ))
                connection.commit()
                return cursor.lastrowid
        except pymysql.IntegrityError as e:
            raise DatabaseException(f"Erro de integridade: {str(e)}")
        except pymysql.Error as e:
            raise DatabaseException(f"Erro ao criar agendamento: {str(e)}")
        finally:
            connection.close()
    
    def atualizar(self, agendamento):
        """
        Atualiza um agendamento existente
        
        :param agendamento: Objeto Agendamento com dados atualizados
        :return: bool indicando sucesso
        """
        connection = self._get_connection()
        try:
            with connection.cursor() as cursor:
                sql = """
                    UPDATE agendamentos
                    SET inicio = %s, fim = %s, cliente_id = %s, barbeiro_id = %s
                    WHERE id = %s
                """
                cursor.execute(sql, (
                    agendamento.inicio,
                    agendamento.fim,
                    agendamento.cliente_id,
                    agendamento.barbeiro_id,
                    agendamento.id
                ))
                connection.commit()
                
                if cursor.rowcount == 0:
                    raise NotFoundException("Agendamento não encontrado")
                
                return True
        except pymysql.Error as e:
            raise DatabaseException(f"Erro ao atualizar agendamento: {str(e)}")
        finally:
            connection.close()
    
    def deletar(self, agendamento_id):
        """
        Deleta um agendamento
        
        :param agendamento_id: ID do agendamento
        :return: bool indicando sucesso
        """
        connection = self._get_connection()
        try:
            with connection.cursor() as cursor:
                sql = "DELETE FROM agendamentos WHERE id = %s"
                cursor.execute(sql, (agendamento_id,))
                connection.commit()
                
                if cursor.rowcount == 0:
                    raise NotFoundException("Agendamento não encontrado")
                
                return True
        except pymysql.Error as e:
            raise DatabaseException(f"Erro ao deletar agendamento: {str(e)}")
        finally:
            connection.close()


# Instância singleton
agendamento_db_repository = AgendamentoDBRepository()
