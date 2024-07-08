import logging
import subprocess
import os
import getpass

def run(source_db_info):
    logging.info(f"Exporting schema from source database: {source_db_info['name']}")
    
    password = source_db_info.get('password')
    
    if not password:
        # Prompt for the password securely if not provided
        password = getpass.getpass(prompt='Enter the PostgreSQL password: ')
        
    # Set the environment variable for the password
    env = {**os.environ, 'PGPASSWORD': password}
    
    # Construct the output file name based on the database name
    output_file = f"{source_db_info['name']}_schema.sql"
    
    # Construct the pg_dump command
    command = f'pg_dump -U {source_db_info["user"]} -h {source_db_info["host"]} -p {source_db_info["port"]} --schema-only {source_db_info["name"]} > {output_file}'

    try:
        # Run the pg_dump command
        result = subprocess.run(command, env=env, shell=True, check=True, text=True, capture_output=True)
        
        # Check for any errors
        if result.returncode == 0:
            logging.info(f'Schema exported successfully to {output_file}')
        else:
            logging.error(f'Error occurred: {result.stderr}')
    except subprocess.CalledProcessError as e:
        logging.error(f'Error during schema export: {e.stderr}')
    except Exception as e:
        logging.error(f'Unexpected error: {e}')

