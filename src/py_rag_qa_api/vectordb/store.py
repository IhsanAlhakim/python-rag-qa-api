from py_rag_qa_api.config.settings import Config
import psycopg2
import os

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