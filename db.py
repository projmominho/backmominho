import os
import psycopg2
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env para o ambiente
# Isso é necessário apenas localmente para evitar expor credenciais no código.
load_dotenv()


def get_connection():
    """
    Estabelece e retorna a conexão com o banco de dados PostgreSQL.
    As credenciais são obtidas a partir das variáveis de ambiente (.env).
    """
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),  # Endereço do host do banco de dados
        port=os.getenv("DB_PORT", 5432),  # Porta do banco de dados
        dbname=os.getenv("DB_NAME"),  # Nome do banco de dados
        user=os.getenv("DB_USER"),  # Nome de usuário para conexão
        password=os.getenv("DB_PASSWORD"),  # Senha do banco de dados
    )


def get_rows(query, params=None):
    """
    Executa uma consulta SQL e retorna todas as linhas (registros) da consulta.
    Recebe a consulta SQL como string e os parâmetros (se houver) para execução.
    """
    conn = get_connection()  # Estabelece a conexão com o banco
    cur = conn.cursor()  # Cria um cursor para executar a consulta

    # Executa a consulta passando os parâmetros (se houver)
    cur.execute(query, params or ())

    # Obtém todas as linhas retornadas pela consulta
    rows = cur.fetchall()

    # Fecha o cursor e a conexão com o banco de dados
    cur.close()
    conn.close()

    return rows  # Retorna as linhas obtidas da consulta
