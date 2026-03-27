import os
import pytest
import pymysql
from pymysql.constants import CLIENT

# Força a variável de ambiente para que DBConnection a utilize (e força host local para rodar pytest)
os.environ['MYSQL_DATABASE'] = 'barbearia_test_db'
os.environ['MYSQL_HOST'] = '127.0.0.1'

@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    import dotenv
    env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
    dotenv.load_dotenv(dotenv_path=env_path)

    os.environ['MYSQL_HOST'] = '127.0.0.1'
    os.environ['MYSQL_DATABASE'] = 'barbearia_test_db'

    host = '127.0.0.1'
    port = int(os.getenv("MYSQL_PORT", "3306"))
    user = os.getenv("DB_USER_ROOT", "root")
    password = os.getenv("MYSQL_ROOT_PASSWORD", "sua_senha_segura") 
    
    try:
        conn = pymysql.connect(host=host, port=port, user=user, password=password)
    except pymysql.Error:
        user = os.getenv("MYSQL_USER", "barbearia_user")
        password = os.getenv("MYSQL_PASSWORD", "")
        conn = pymysql.connect(host=host, port=port, user=user, password=password)
        
    try:
        with conn.cursor() as cursor:
            cursor.execute("DROP DATABASE IF EXISTS barbearia_test_db")
            cursor.execute("CREATE DATABASE barbearia_test_db")
            cursor.execute(f"GRANT ALL PRIVILEGES ON barbearia_test_db.* TO '{os.getenv('MYSQL_USER', 'barbearia_user')}'@'%'")
            conn.commit()
    finally:
        conn.close()
        
    schema_path = os.path.join(os.path.dirname(__file__), '..', 'database_schema.sql')
    with open(schema_path, 'r', encoding='utf-8') as f:
        schema_sql = f.read()
        
    conn = pymysql.connect(
        host=host, port=port, user=user, password=password, database='barbearia_test_db',
        client_flag=CLIENT.MULTI_STATEMENTS
    )
    try:
        with conn.cursor() as cursor:
            cursor.execute(schema_sql)
            conn.commit()
    finally:
        conn.close()

@pytest.fixture(autouse=True)
def limpa_tabelas():
    from config.database import DBConnection
    db = DBConnection()
    conn = db.get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
            cursor.execute("TRUNCATE TABLE agendamentos;")
            cursor.execute("TRUNCATE TABLE clientes;")
            cursor.execute("TRUNCATE TABLE empresa;")
            cursor.execute("INSERT INTO empresa (nome, descricao, endereco, cnpj, telefone, email) VALUES ('Minha Barbearia', 'Barbearia moderna com os melhores profissionais.', 'Rua Exemplo, 123 - Centro', '00.000.000/0001-00', '(00) 00000-0000', 'contato@minhabarbearia.com')")
            cursor.execute("TRUNCATE TABLE funcionarios;")
            cursor.execute("TRUNCATE TABLE horarios_funcionamento;")
            cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
            conn.commit()
    finally:
        conn.close()
