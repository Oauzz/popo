import logging
import sqlparse
import re
import os
import json

def extract_foreign_keys(schema):
    foreign_keys = {}

    statements = sqlparse.parse(schema)
    for stmt in statements:
        if stmt.get_type() == 'CREATE':
            table_name = None
            for token in stmt.tokens:
                if isinstance(token, sqlparse.sql.Identifier):
                    table_name = token.get_real_name()
                    if table_name.startswith('public.'):
                        table_name = table_name[len('public.'):]
                    break
            if table_name:
                foreign_keys[table_name] = []
                for token in stmt.tokens:
                    if isinstance(token, sqlparse.sql.Parenthesis):
                        fk_tokens = token.value.split(",")
                        for fk_token in fk_tokens:
                            if 'REFERENCES' in fk_token.upper():
                                match = re.search(r'REFERENCES\s+(\S+)\s*\((\S+)\)', fk_token, re.IGNORECASE)
                                if match:
                                    referenced_table = match.group(1)
                                    if referenced_table.startswith('public.'):
                                        referenced_table = referenced_table[len('public.'):]
                                    foreign_keys[table_name].append(referenced_table)
    return foreign_keys

def run(merged_schema_file):
    logging.info(f"Extracting foreign keys from merged schema file: {merged_schema_file}")

    try:
        with open(merged_schema_file, 'r') as file:
            schema = file.read()

        foreign_keys = extract_foreign_keys(schema)
        if foreign_keys:
            base_name = os.path.splitext(os.path.basename(merged_schema_file))[0]
            output_file = f"{base_name}_foreign_keys.json"
            with open(output_file, 'w') as f:
                json.dump(foreign_keys, f, indent=4)
            logging.info(f"Foreign keys written to {output_file}")
        return foreign_keys

    except FileNotFoundError:
        logging.error(f"File {merged_schema_file} not found.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    merged_schema_file = "merged_schema.sql"
    run(merged_schema_file)
