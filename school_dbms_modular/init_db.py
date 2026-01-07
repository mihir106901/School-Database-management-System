"""Initialize database + tables if they do not exist.

This script reads connection info from environment variables or a .env file.
It executes SQL scripts in ./sql in order:
- 00_create_db.sql
- 01_tables.sql
"""
from school_dbms.config import load_config
from school_dbms.db import connect_server, run_sql_script

def main():
    cfg = load_config()
    # Connect without specifying database first (server-level)
    cnx = connect_server(cfg)
    try:
        run_sql_script(cnx, "sql/00_create_db.sql", cfg)
        run_sql_script(cnx, "sql/01_tables.sql", cfg)
        print("✅ Database and tables initialized successfully.")
    finally:
        cnx.close()

if __name__ == "__main__":
    main()
