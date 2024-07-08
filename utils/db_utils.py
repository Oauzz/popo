import logging
import psycopg2
from psycopg2 import sql

def create_database(db_name, user, password, host='localhost', port='5432'):
    try:
        # Connect to PostgreSQL server
        connection = psycopg2.connect(
            user=user,
            password=password,
            host=host,
            port=port
        )
        connection.autocommit = True
        cursor = connection.cursor()
        
        # Create new database
        cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db_name)))
        logging.info(f"Database {db_name} created successfully")
        
    except Exception as error:
        logging.error(f"Error creating database {db_name}: {error}")
    finally:
        if connection:
            cursor.close()
            connection.close()
