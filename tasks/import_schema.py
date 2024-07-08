import logging
import subprocess
import os
import getpass

def run(new_db_info, source_db_name):
    logging.info(f"Importing schema into new database: {new_db_info['name']}")

    password = new_db_info.get('password')
    
    if not password:
        # Prompt for the password securely if not provided
        password = getpass.getpass(prompt='Enter the PostgreSQL password: ')

    # Set the environment variable for the password
    env = {**os.environ, 'PGPASSWORD': password}
    
    # Construct the schema file name based on the database name
    schema_file = f"{source_db_name}_schema.sql"
    
    # Construct the psql command
    command = f'psql -U {new_db_info["user"]} -h {new_db_info["host"]} -p {new_db_info["port"]} -d {new_db_info["name"]} -f {schema_file}'

    try:
        # Run the psql command
        result = subprocess.run(command, env=env, shell=True, check=True, text=True, capture_output=True)
        
        # Check for any errors
        if result.returncode == 0:
            logging.info(f'Schema imported successfully from {schema_file}')
        else:
            logging.error(f'Error occurred: {result.stderr}')
    except subprocess.CalledProcessError as e:
        logging.error(f'Error during schema import: {e.stderr}')
    except Exception as e:
        logging.error(f'Unexpected error: {e}')

