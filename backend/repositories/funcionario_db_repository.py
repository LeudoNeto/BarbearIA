from models.funcionario import Funcionario
from config.database import DBConnection
from exceptions import DatabaseException, DuplicateException
import pymysql


class FuncionarioDBRepository:
    """Repositório para operações de persistência de Funcionario em banco de dados"""
    
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
        Lista todos os funcionários
        
        :return: Lista de objetos Funcionario
        """
        connection = self._get_connection()
        try:
            with connection.cursor() as cursor:
                sql = """
                    SELECT id, email, senha, foto, eh_barbeiro, eh_admin 
                    FROM funcionarios
                """
                cursor.execute(sql)
                results = cursor.fetchall()
                
                funcionarios = []
                for row in results:
                    funcionario = Funcionario(
                        id=row['id'],
                        email=row['email'],
                        senha=row['senha'],
                        foto=row['foto'],
                        eh_barbeiro=bool(row['eh_barbeiro']),
                        eh_admin=bool(row['eh_admin'])
                    )
                    funcionarios.append(funcionario)
                
                return funcionarios
        except pymysql.Error as e:
            raise DatabaseException(f"Erro ao listar funcionários: {str(e)}")
        finally:
            connection.close()
    
    def buscar_por_id(self, funcionario_id):
        """
        Busca um funcionário pelo ID
        
        :param funcionario_id: ID do funcionário
        :return: Objeto Funcionario ou None se não encontrado
        """
        connection = self._get_connection()
        try:
            with connection.cursor() as cursor:
                sql = """
                    SELECT id, email, senha, foto, eh_barbeiro, eh_admin 
                    FROM funcionarios
                    WHERE id = %s
                """
                cursor.execute(sql, (funcionario_id,))
                row = cursor.fetchone()
                
                if row is None:
                    return None
                
                return Funcionario(
                    id=row['id'],
                    email=row['email'],
                    senha=row['senha'],
                    foto=row['foto'],
                    eh_barbeiro=bool(row['eh_barbeiro']),
                    eh_admin=bool(row['eh_admin'])
                )
        except pymysql.Error as e:
            raise DatabaseException(f"Erro ao buscar funcionário por ID: {str(e)}")
        finally:
            connection.close()
    
    def buscar_por_email(self, email):
        """
        Busca um funcionário pelo email
        
        :param email: Email do funcionário
        :return: Objeto Funcionario ou None se não encontrado
        """
        connection = self._get_connection()
        try:
            with connection.cursor() as cursor:
                sql = """
                    SELECT id, email, senha, foto, eh_barbeiro, eh_admin 
                    FROM funcionarios
                    WHERE email = %s
                """
                cursor.execute(sql, (email,))
                row = cursor.fetchone()
                
                if row is None:
                    return None
                
                return Funcionario(
                    id=row['id'],
                    email=row['email'],
                    senha=row['senha'],
                    foto=row['foto'],
                    eh_barbeiro=bool(row['eh_barbeiro']),
                    eh_admin=bool(row['eh_admin'])
                )
        except pymysql.Error as e:
            raise DatabaseException(f"Erro ao buscar funcionário por email: {str(e)}")
        finally:
            connection.close()
    
    def criar(self, funcionario):
        """
        Cria um novo funcionário no banco de dados
        
        :param funcionario: Objeto Funcionario
        :return: ID do funcionário criado
        """
        connection = self._get_connection()
        try:
            with connection.cursor() as cursor:
                sql = """
                    INSERT INTO funcionarios (email, senha, foto, eh_barbeiro, eh_admin)
                    VALUES (%s, %s, %s, %s, %s)
                """
                cursor.execute(sql, (
                    funcionario.email,
                    funcionario.senha,
                    funcionario.foto,
                    funcionario.eh_barbeiro,
                    funcionario.eh_admin
                ))
                connection.commit()
                return cursor.lastrowid
        except pymysql.IntegrityError as e:
            # Verificar se é erro de duplicação de email
            if 'email' in str(e).lower() and 'duplicate' in str(e).lower():
                raise DuplicateException("Este email já está cadastrado no sistema")
            raise DatabaseException(f"Erro de integridade: {str(e)}")
        except pymysql.Error as e:
            raise DatabaseException(f"Erro ao criar funcionário: {str(e)}")
        finally:
            connection.close()
    
    def contar(self):
        """
        Conta o número total de funcionários no banco de dados
        
        :return: int com a quantidade de funcionários
        """
        connection = self._get_connection()
        try:
            with connection.cursor() as cursor:
                sql = "SELECT COUNT(*) as total FROM funcionarios"
                cursor.execute(sql)
                row = cursor.fetchone()
                return row['total']
        except pymysql.Error as e:
            raise DatabaseException(f"Erro ao contar funcionários: {str(e)}")
        finally:
            connection.close()


# Instância singleton
funcionario_db_repository = FuncionarioDBRepository()
