from py_rag_qa_api.core.config import Config
import psycopg2.pool

def createDBConnPool(cfg: Config) -> psycopg2.pool.ThreadedConnectionPool:
    try:
        dbConnPool = psycopg2.pool.ThreadedConnectionPool(
            minconn=2,
            maxconn=10,
            user=cfg.dbUser,
            password=cfg.dbPass,
            host=cfg.dbHost,
            port=cfg.dbPort,
            dbname=cfg.dbName
        )
        print("connection pool ready...")
        return dbConnPool
    except Exception as e:
        print(f"failed to connect to the database: {e}")
        raise

def connect(cfg: Config) -> psycopg2.extensions.connection:
    try:
        conn = psycopg2.connect(
            user=cfg.dbUser,
            password=cfg.dbPass,
            host=cfg.dbHost,
            port=cfg.dbPort,
            dbname=cfg.dbName
        )
        print("Connection successful")
        return conn
    except Exception as e:
        print(f"failed to connect to the database: {e}")
        raise