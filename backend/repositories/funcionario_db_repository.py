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


# Instância singleton
funcionario_db_repository = FuncionarioDBRepository()
