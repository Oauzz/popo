import logging
from utils.db_utils import create_database

def run(db_info):
    logging.info(f"Creating new database: {db_info['name']}")
    create_database(db_info['name'], db_info['user'], db_info['password'], db_info['host'], db_info['port'])
