import logging
import sqlparse
import re
import os
import json

def extract_columns_types(schema):
    columns_types = {}

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
                columns_types[table_name] = {'columns': [], 'types': []}
                for token in stmt.tokens:
                    if isinstance(token, sqlparse.sql.Parenthesis):
                        column_tokens = token.value.split(",")
                        for column_token in column_tokens:
                            column_details = column_token.strip().split()
                            if 'REFERENCES' not in column_token.upper():
                                column_name = column_details[0].strip('"')
                                column_type = column_details[1].strip().lower()
                                columns_types[table_name]['columns'].append(column_name)
                                columns_types[table_name]['types'].append(get_python_type(column_type))
    return columns_types

def get_python_type(sql_type):
    sql_type = sql_type.lower()
    if sql_type in ['smallint', 'integer', 'bigint', 'int2', 'int4', 'int8']:
        return 'int'
    elif sql_type in ['decimal', 'numeric', 'real', 'double precision', 'float4', 'float8']:
        return 'float'
    elif sql_type in ['char', 'character', 'varchar', 'character varying', 'text', 'name']:
        return 'str'
    elif sql_type in ['boolean', 'bool']:
        return 'bool'
    elif sql_type in ['date', 'timestamp', 'timestamp without time zone', 'timestamp with time zone', 'time', 'time without time zone', 'time with time zone']:
        return 'datetime'
    elif sql_type in ['bytea']:
        return 'bytes'
    elif sql_type in ['uuid']:
        return 'uuid'
    elif sql_type in ['json', 'jsonb']:
        return 'json'
    elif sql_type in ['xml']:
        return 'xml'
    elif sql_type in ['array']:
        return 'array'
    elif sql_type in ['tsvector']:
        return 'tsvector'
    else:
        return 'str'


def run(merged_schema_file):
    logging.info(f"Extracting columns and types from merged schema file: {merged_schema_file}")

    try:
        with open(merged_schema_file, 'r') as file:
            schema = file.read()

        columns_types = extract_columns_types(schema)
        
        if columns_types:
            base_name = os.path.splitext(os.path.basename(merged_schema_file))[0]
            output_file_ct = f"{base_name}_columns_types.json"
            with open(output_file_ct, 'w') as f:
                json.dump(columns_types, f, indent=4)
            logging.info(f"Columns and types written to {output_file_ct}")
        
        return columns_types

    except FileNotFoundError:
        logging.error(f"File {merged_schema_file} not found.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    merged_schema_file = "merged_schema.sql"
    run(merged_schema_file)
