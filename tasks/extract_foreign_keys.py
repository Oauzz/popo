import logging
import sqlparse
import re
import os
import json

def extract_foreign_keys(merged_schema_file):
    foreign_keys = {}

    try:
        with open(merged_schema_file, 'r') as file:
            schema = file.read()
        
        statements = sqlparse.parse(schema)
        
        for stmt in statements:
            if stmt.get_type() == 'CREATE':
                table_name = None
                for token in stmt.tokens:
                    if isinstance(token, sqlparse.sql.Identifier):
                        table_name = token.get_real_name()
                        break
                if table_name:
                    foreign_keys[table_name] = []
                    for token in stmt.tokens:
                        if isinstance(token, sqlparse.sql.Parenthesis):
                            fk_tokens = token.value.split(",")
                            for fk_token in fk_tokens:
                                if 'REFERENCES' in fk_token.upper():
                                    match = re.search(r'REFERENCES\s+(\S+)', fk_token, re.IGNORECASE)
                                    if match:
                                        referenced_table = match.group(1)
                                        foreign_keys[table_name].append(referenced_table)
                                        
        return foreign_keys

    except FileNotFoundError:
        logging.error(f"File {merged_schema_file} not found.")
        return None
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return None

def run(merged_schema_file):
    logging.info(f"Extracting foreign keys from merged schema file: {merged_schema_file}")

    foreign_keys = extract_foreign_keys(merged_schema_file)
    if foreign_keys is not None:
        # Extract the base name of the merged schema file to use in the output filename
        base_name = os.path.splitext(os.path.basename(merged_schema_file))[0]
        output_file = f"{base_name}_foreign_keys.json"
        
        with open(output_file, 'w') as f:
            json.dump(foreign_keys, f, indent=4)
        
        logging.info(f"Foreign keys written to {output_file}")

    return foreign_keys

if __name__ == "__main__":
    # Example usage:
    merged_schema_file = "merged_schema.sql"
    run(merged_schema_file)
