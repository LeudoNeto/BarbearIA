from models.cliente import Cliente
from config.database import DBConnection
from exceptions import DatabaseException, DuplicateException
import pymysql


class ClienteDBRepository:
    """Repositório para operações de persistência de Cliente em banco de dados"""
    
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
        Lista todos os clientes
        
        :return: Lista de objetos Cliente
        """
        connection = self._get_connection()
        try:
            with connection.cursor() as cursor:
                sql = """
                    SELECT id, email, senha, foto, telefone 
                    FROM clientes
                """
                cursor.execute(sql)
                results = cursor.fetchall()
                
                clientes = []
                for row in results:
                    cliente = Cliente(
                        id=row['id'],
                        email=row['email'],
                        senha=row['senha'],
                        foto=row['foto'],
                        telefone=row['telefone']
                    )
                    clientes.append(cliente)
                
                return clientes
        except pymysql.Error as e:
            raise DatabaseException(f"Erro ao listar clientes: {str(e)}")
        finally:
            connection.close()
    
    def buscar_por_id(self, cliente_id):
        """
        Busca um cliente pelo ID
        
        :param cliente_id: ID do cliente
        :return: Objeto Cliente ou None se não encontrado
        """
        connection = self._get_connection()
        try:
            with connection.cursor() as cursor:
                sql = """
                    SELECT id, email, senha, foto, telefone 
                    FROM clientes
                    WHERE id = %s
                """
                cursor.execute(sql, (cliente_id,))
                row = cursor.fetchone()
                
                if row is None:
                    return None
                
                return Cliente(
                    id=row['id'],
                    email=row['email'],
                    senha=row['senha'],
                    foto=row['foto'],
                    telefone=row['telefone']
                )
        except pymysql.Error as e:
            raise DatabaseException(f"Erro ao buscar cliente por ID: {str(e)}")
        finally:
            connection.close()
    
    def buscar_por_email(self, email):
        """
        Busca um cliente pelo email
        
        :param email: Email do cliente
        :return: Objeto Cliente ou None se não encontrado
        """
        connection = self._get_connection()
        try:
            with connection.cursor() as cursor:
                sql = """
                    SELECT id, email, senha, foto, telefone 
                    FROM clientes
                    WHERE email = %s
                """
                cursor.execute(sql, (email,))
                row = cursor.fetchone()
                
                if row is None:
                    return None
                
                return Cliente(
                    id=row['id'],
                    email=row['email'],
                    senha=row['senha'],
                    foto=row['foto'],
                    telefone=row['telefone']
                )
        except pymysql.Error as e:
            raise DatabaseException(f"Erro ao buscar cliente por email: {str(e)}")
        finally:
            connection.close()
    
    def criar(self, cliente):
        """
        Cria um novo cliente no banco de dados
        
        :param cliente: Objeto Cliente
        :return: ID do cliente criado
        """
        connection = self._get_connection()
        try:
            with connection.cursor() as cursor:
                sql = """
                    INSERT INTO clientes (email, senha, foto, telefone)
                    VALUES (%s, %s, %s, %s)
                """
                cursor.execute(sql, (
                    cliente.email,
                    cliente.senha,
                    cliente.foto,
                    cliente.telefone
                ))
                connection.commit()
                return cursor.lastrowid
        except pymysql.IntegrityError as e:
            # Verificar se é erro de duplicação de email
            if 'email' in str(e).lower() and 'duplicate' in str(e).lower():
                raise DuplicateException("Este email já está cadastrado no sistema")
            raise DatabaseException(f"Erro de integridade: {str(e)}")
        except pymysql.Error as e:
            raise DatabaseException(f"Erro ao criar cliente: {str(e)}")
        finally:
            connection.close()


# Instância singleton
cliente_db_repository = ClienteDBRepository()
