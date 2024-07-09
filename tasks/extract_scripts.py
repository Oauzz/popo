import logging
import sqlparse
import os

def extract_table_statements(schema):
    statements = sqlparse.parse(schema)
    table_statements = {}
    alter_statements = []

    for stmt in statements:
        if stmt.get_type() == 'CREATE' and any(token.value.upper() == 'TABLE' for token in stmt.tokens if isinstance(token, sqlparse.sql.Token)):
            table_name = None
            for token in stmt.tokens:
                if isinstance(token, sqlparse.sql.Identifier):
                    table_name = token.get_real_name()
                    break
            if table_name:
                table_statements[table_name] = str(stmt)
        elif stmt.get_type() == 'ALTER':
            alter_statements.append(stmt)

    return table_statements, alter_statements

def merge_statements(table_statements, alter_statements):
    for stmt in alter_statements:
        table_name = None
        alter_parts = []

        for token in stmt.tokens:
            if token.ttype == sqlparse.tokens.Keyword and token.value.upper() == 'TABLE':
                table_name = next(t for t in stmt.tokens if isinstance(t, sqlparse.sql.Identifier)).get_real_name()
            if token.ttype == sqlparse.tokens.Keyword and token.value.upper() == 'ADD':
                alter_parts.append('ADD')
            elif alter_parts:
                alter_parts[-1] += ' ' + str(token).strip()
                
        if table_name and table_name in table_statements:
            create_statement = table_statements[table_name]
            create_statement = create_statement.rstrip(");")  # Remove the last ");" to append constraints
            constraint_str = ' '.join(alter_parts).replace('ADD', ',').replace(' ,', ',').strip()
            constraint_str = constraint_str.replace(' ,', ',').replace('( ', '(').replace(' )', ')')
            create_statement += ' ' + constraint_str + ");"
            table_statements[table_name] = create_statement

    return table_statements

def run(schema_file):
    logging.info(f"Extracting table scripts from schema file: {schema_file}")

    try:
        with open(schema_file, 'r') as file:
            schema = file.read()

        table_statements, alter_statements = extract_table_statements(schema)
        merged_statements = merge_statements(table_statements, alter_statements)
        
        # Extract the base name of the schema file to use in the output filename
        base_name = os.path.splitext(os.path.basename(schema_file))[0]
        output_file = f"{base_name}_merged_schema.sql"
        
        with open(output_file, 'w') as f:
            for table_name, stmt in merged_statements.items():
                f.write(stmt + "\n\n")

        logging.info(f"Merged CREATE TABLE statements written to {output_file}")
        return merged_statements, base_name

    except FileNotFoundError:
        logging.error(f"File {schema_file} not found.")
        return None, None
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return None, None
