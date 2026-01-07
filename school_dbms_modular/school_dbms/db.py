from __future__ import annotations
import os
from pathlib import Path
import mysql.connector
from mysql.connector.connection import MySQLConnection
from .config import DBConfig

def connect_server(cfg: DBConfig) -> MySQLConnection:
    """Connect to MySQL server (without selecting a database)."""
    return mysql.connector.connect(
        host=cfg.host,
        user=cfg.user,
        password=cfg.password,
    )

def connect_db(cfg: DBConfig) -> MySQLConnection:
    """Connect to MySQL server and select database."""
    return mysql.connector.connect(
        host=cfg.host,
        user=cfg.user,
        password=cfg.password,
        database=cfg.database,
    )

def run_sql_script(cnx: MySQLConnection, script_path: str, cfg: DBConfig) -> None:
    """Run a SQL file. Supports {{DB_NAME}} template."""
    path = Path(script_path)
    if not path.is_absolute():
        # script_path is relative to project root
        path = Path(__file__).resolve().parent.parent / path

    sql = path.read_text(encoding="utf-8")
    sql = sql.replace("{{DB_NAME}}", cfg.database)
    
    # Remove SQL comments
    lines = sql.split('\n')
    lines = [line for line in lines if not line.strip().startswith('--')]
    sql = '\n'.join(lines)

    cur = cnx.cursor()
    try:
        # If this is the tables script, ensure we USE the DB first.
        if path.name == "01_tables.sql":
            cur.execute(f"USE `{cfg.database}`;")
        # Split SQL into individual statements and execute each
        statements = [stmt.strip() for stmt in sql.split(';') if stmt.strip()]
        for stmt in statements:
            if stmt:
                cur.execute(stmt)
        cnx.commit()
    finally:
        cur.close()

def exec_query(cnx: MySQLConnection, sql: str, params=None, fetch: str | None = None):
    """Execute a query with params.
    fetch: None | 'one' | 'all'
    """
    cur = cnx.cursor()
    try:
        cur.execute(sql, params or ())
        if fetch == "one":
            return cur.fetchone()
        if fetch == "all":
            return cur.fetchall(), [d[0] for d in cur.description]
        cnx.commit()
        return None
    finally:
        cur.close()
