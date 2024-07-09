import logging
import random
import json
from faker import Faker

fake = Faker()

def generate_dummy_data(schema_file, foreign_keys_file, order_file, num_rows=10):
    with open(schema_file, 'r') as file:
        schema = json.load(file)
    
    with open(foreign_keys_file, 'r') as file:
        foreign_keys = json.load(file)

    with open(order_file, 'r') as file:
        table_order = file.read().splitlines()

    dummy_data = {}
    reference_data = {}

    for table in table_order:
        columns = schema[table]['columns']
        types = schema[table]['types']
        table_data = []

        for _ in range(num_rows):
            row = []
            for col, col_type in zip(columns, types):
                if col in foreign_keys.get(table, []):
                    parent_table = [key for key, value in foreign_keys.items() if table in value][0]
                    row.append(random.choice(reference_data[parent_table])[0])
                else:
                    row.append(generate_value(col_type))
            table_data.append(row)
        
        dummy_data[table] = {
            'columns': columns,
            'rows': table_data
        }
        reference_data[table] = [row for row in table_data if 'id' in schema[table]['columns'][0]]

    output_file = schema_file.replace('_columns_types.json', '_dummy_data.json')
    with open(output_file, 'w') as f:
        json.dump(dummy_data, f, indent=4)
    logging.info(f"Dummy data written to {output_file}")
    
    return dummy_data

def generate_value(col_type):
    if col_type == 'int':
        return random.randint(1, 1000)
    elif col_type == 'float':
        return round(random.uniform(1.0, 100.0), 2)
    elif col_type == 'str':
        return fake.text(max_nb_chars=20)
    elif col_type == 'bool':
        return fake.boolean()
    elif col_type == 'datetime':
        return fake.date_time_this_decade().isoformat()
    elif col_type == 'bytes':
        return fake.binary(length=10).decode('latin1')
    elif col_type == 'uuid':
        return str(fake.uuid4())
    elif col_type == 'json':
        return json.dumps({"key": "value"})
    elif col_type == 'xml':
        return '<root><key>value</key></root>'
    elif col_type == 'array':
        return [fake.word() for _ in range(3)]
    elif col_type == 'tsvector':
        return fake.sentence()
    else:
        return fake.text(max_nb_chars=20)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    schema_file = "merged_schema_columns_types.json"
    foreign_keys_file = "merged_schema_foreign_keys.json"
    order_file = "table_order.txt"
    generate_dummy_data(schema_file, foreign_keys_file, order_file)
